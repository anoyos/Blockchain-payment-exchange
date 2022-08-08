import logging
import time
import random
from decimal import Decimal
from typing import Union

from api_contrib.core.utils import logger

from app import crud
from app import models
from app.connections import mq
from app.core import constants
from app.core.config import settings
from app.market.core.depth import MarketOrderDepth
from app.market.core.events import process_market_deal, change_balances, update_market_depth
from app.tasks.jobs.tools import get_prices, _define_size_for_auto_trade

logger.setLevel(logging.INFO)


class MarketBroker:

    def __init__(self, market: models.Market) -> None:
        self.market = market
        self.depth = MarketOrderDepth(market)

    def _replace_order(self, order: models.Order, trade_size: Decimal) -> str:
        """
            1) Update order volume by quantity remained after trade.
            2) Remove satisfied order from queue (market depth)
        """
        order_status = models.OrderStatus.NEW
        try:
            size_delta = abs(order.quantity - trade_size)
            if size_delta != 0:
                order_status = models.OrderStatus.PARTIAL_EXECUTED
                crud.order.update_by_kwargs(order, quantity=size_delta, status=order_status)

            else:
                order_status = models.OrderStatus.EXECUTED
                crud.order.update_by_kwargs(order, status=order_status)
                self.depth.delete(order)

        except Exception as e:
            logger.error(e, exc_info=True)

        return order_status

    @staticmethod
    def _get_commission_size(order: models.Order, trade_value: Decimal) -> Decimal:
        if order.user_id == constants.DEALER_USER_ID:
            return Decimal(0)
        else:
            return Decimal(trade_value) * Decimal(settings.COMMISSION_PERCENT)

    def _create_trade(self, order: models.Order, trade_size: Decimal) -> models.Trade:
        trade_value = Decimal(order.price) * Decimal(trade_size)
        # commission = trade_value * settings.COMMISSION_PERCENT
        trade = models.Trade(
            user_id=order.user_id,
            side=order.side,
            symbol=order.symbol,
            price=order.price,
            quantity=trade_size,
            value=trade_value,
            commission=self._get_commission_size(order, trade_value),
            base_currency_id=self.market.base_currency_id,
            base_currency_code=self.market.base_currency_code,
            quote_currency_id=self.market.quote_currency_id,
            quote_currency_code=self.market.quote_currency_code,
            order_id=order.id
        )
        row_id = crud.trade.insert_one_sync(trade)
        trade.id = row_id
        return trade

    def _get_or_delete_order(self, order_id: bytes, side: str) -> Union[models.Order, None]:
        obj_id = order_id.decode()
        order = crud.order.find_one_sync({'id': obj_id})
        if order:
            return models.Order(**order)
        else:
            logger.warning(f"Order {order_id} not found in DB. Deleted from queue")
            queue = self.depth.get_queue(side)
            queue.delete(obj_id)
            return None

    def create_order(self, new_order: models.Order):
        new_order.id = crud.order.insert_one_sync(new_order)

        # Place order into Market depth
        self.depth.push(new_order)
        update_market_depth(new_order)

    def cancel_order(self, order: models.Order):
        order.status = models.OrderStatus.CANCELED

        # Remove from Redis Zrange
        self.depth.delete(order)

        # Remove from order_book and push event
        update_market_depth(order)

        # Save status in DB
        crud.order.update_obj_sync(order, {
            'status': order.status
        })

        mq.publisher.send_event("change_order_status_event", order.dict())

    def cancel_unfilled_orders(self):
        """ Cancel orders if doesnt match """
        orders = crud.order.find_all_sync({
            "symbol": self.market.symbol,
            "status": {"$in": [models.OrderStatus.NEW, models.OrderStatus.PARTIAL_EXECUTED]},
            "time_in_force": models.TimeInForce.FOK
        })
        for order_document in orders:
            self.cancel_order(models.Order(**order_document))

    def generate_orders(self):

        quote_currency = settings.ASSETS[self.market.quote_currency_code]['main_net_code']
        prices = get_prices(quote_currency)
        self.cancel_unfilled_orders()
        external_price = prices[self.market.symbol]

        price = Decimal(external_price) * Decimal(round(random.uniform(1.01, 1.02), 4))

        for side in [models.TradeType.BUY, models.TradeType.SELL]:
            order_size = _define_size_for_auto_trade(self.market, price, constants.ALL_MARKETS)
            self.create_order(models.Order(**{
                "user_id": constants.DEALER_USER_ID,
                "symbol": self.market.symbol,
                "side": side,
                "quantity": order_size,
                "price": price,
                "time_in_force": models.order.TimeInForce.FOK
            }))

            # Create order for mock fill order book
            dvg_direction = -1 if side == models.TradeType.BUY else 1
            for prc_dev in [0.02, 0.03]:
                self.create_order(models.Order(**{
                    "user_id": constants.DEALER_USER_ID,
                    "symbol": self.market.symbol,
                    "side": side,
                    "quantity": order_size,
                    "price": Decimal(price) * (1 + dvg_direction * Decimal(prc_dev)),
                    "time_in_force": models.order.TimeInForce.FOK
                }))

    def _execute(self, buy_order: models.Order, sell_order: models.Order) -> bool:
        try:
            trade_size = min(sell_order.quantity, buy_order.quantity)
            for order in [buy_order, sell_order]:
                # Update order status
                order.status = self._replace_order(order, trade_size)
                # create trade record
                trade = self._create_trade(order, trade_size)

                # Send change balance message
                result = change_balances(trade)

                # Push event to other services
                process_market_deal(order, trade)
        except Exception as e:
            logger.error(e, exc_info=True)
            return False

        # Return order status
        return True if result['status'] == 'success' else False

    def _execute_orders(self) -> None:
        # logger.info(f"Checking new orders for {self.market.market_name}")

        sell_order_id, lowest_sell_price = self.depth.get_first_by_side(models.TradeType.SELL)
        buy_order_id, highest_buy_price_raw = self.depth.get_first_by_side(models.TradeType.BUY)

        # print(f"sell_order_id, lowest_sell_price : {sell_order_id, lowest_sell_price}")
        # print(f"buy_order_id, highest_buy_price_raw : {buy_order_id, highest_buy_price_raw}")
        highest_buy_price = abs(highest_buy_price_raw)

        if not sell_order_id or not buy_order_id:
            logger.debug(f"{self.market.market_name}: Not enough orders to trade "
                         f"sell_order_id: {sell_order_id}, buy_order_id: {buy_order_id}.")

        elif lowest_sell_price > highest_buy_price:
            logger.info(f"{self.market.market_name}: prices doesn't match. Orders with FOK type will be canceled "
                        f"best_buy: {highest_buy_price}, best_sell: {lowest_sell_price}.")

        else:
            logger.debug(f"{self.market.market_name}: Create trade for orders {buy_order_id}, {sell_order_id}")
            buy_order = self._get_or_delete_order(buy_order_id, models.TradeType.BUY)
            sell_order = self._get_or_delete_order(sell_order_id, models.TradeType.SELL)
            if sell_order and buy_order:
                self._execute(buy_order, sell_order)

    def start(self) -> None:
        while True:
            try:
                self.generate_orders()
                time.sleep(3)
                self._execute_orders()
            except Exception as e:
                logger.error(e, exc_info=True)

    def process_orders(self) -> None:
        try:
            self._execute_orders()
        except Exception as e:
            logger.error(e, exc_info=True)
