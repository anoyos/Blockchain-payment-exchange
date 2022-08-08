from app import models
from app.core import constants
from app.market.core.broker import MarketBroker
from app.tasks.jobs.tools import get_prices, _define_size_for_auto_trade
from decimal import Decimal


def create_orders():
    pass


def create_orders_old():
    for quote_code in ['BTC', 'USDT']:
        prices = get_prices(quote_code)
        for market in constants.ALL_MARKETS:
            if quote_code in market.quote_currency_code:

                broker = MarketBroker(market)
                broker.cancel_unfilled_orders()

                for side in [models.TradeType.BUY, models.TradeType.SELL]:
                    price = prices[market.symbol]
                    order_size = _define_size_for_auto_trade(market, price, constants.ALL_MARKETS)

                    broker.create_order(models.Order(**{
                        "user_id": constants.DEALER_USER_ID,
                        "symbol": market.symbol,
                        "side": side,
                        "quantity": order_size,
                        "price": price,
                        "time_in_force": models.order.TimeInForce.FOK
                    }))

                    # Create order for mock fill order book
                    dvg_direction = -1 if side == models.TradeType.BUY else 1
                    for prc_dev in [0.02, 0.03]:
                        broker.create_order(models.Order(**{
                            "user_id": constants.DEALER_USER_ID,
                            "symbol": market.symbol,
                            "side": side,
                            "quantity": order_size,
                            "price": Decimal(price)*(1 + dvg_direction*Decimal(prc_dev)),
                            "time_in_force": models.order.TimeInForce.FOK
                        }))

                del broker
