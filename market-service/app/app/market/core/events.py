from collections import defaultdict
from datetime import datetime
from decimal import Decimal
from typing import Optional

from api_contrib.core.constants import TradeType

from app import crud
from app.connections import background, mq
from app.core.config import settings
from app.core.constants import get_market_by_symbol, get_market_id_by_symbol
from app.market.core.depth import MarketOrderDepth
from app.models.order import Order
from app.models.trade import Trade


def get_summary(orders, side: str) -> dict:
    result_offers = defaultdict(Decimal)
    max_volume = Decimal(0)
    total_volume = Decimal(0)

    for order in orders:
        volume = order['quantity']

        if volume > max_volume:
            max_volume = volume

        total_volume += volume
        result_offers[order['price']] += volume

    return {
        f'max{side.capitalize()}': max_volume,
        f'total{side.capitalize()}': total_volume,
        f'{side.lower()}': [{
            "price": price,
            "volume": volume,
            "volume_in_quote": volume*price,
        } for price, volume in result_offers.items()
        ]
    }


def update_market_depth(order_in: Order) -> None:
    depth = MarketOrderDepth(get_market_by_symbol(order_in.symbol))

    _, lowest_sell_price = depth.get_first_by_side(TradeType.SELL)
    _, highest_buy_price_raw = depth.get_first_by_side(TradeType.BUY)

    message = {
        "symbol": order_in.symbol,
        "price": abs(highest_buy_price_raw),
        "spread": abs(highest_buy_price_raw) - lowest_sell_price,
    }

    buy_orders = crud.order.find_id_in_sync(depth.buy_queue.all())
    sell_orders = crud.order.find_id_in_sync(depth.sell_queue.all())

    message.update(get_summary(buy_orders, TradeType.BUY))
    message.update(get_summary(sell_orders, TradeType.SELL))

    crud.order_book.collection_sync.update_one({"symbol": order_in.symbol},
                                               {"$set": {"symbol": order_in.symbol, "data": message}},
                                               upsert=True)

    mq.publisher.send_event("orderbook_event", message, room=order_in.symbol)


def update_market_depth_old(order_in: Order) -> None:
    # Find current volume of offers
    query = {
        "symbol": order_in.symbol,
        "side": order_in.side,
        "price": order_in.price,
    }
    _ = crud.market_depth.get_or_create_sync(query)
    # Update volumes
    inc_value = order_in.quantity if order_in.status == 'NEW' else -1 * order_in.quantity
    crud.market_depth.update_by_query_sync(query, {
        "$inc": {
            "volume": inc_value
        }
    })
    # Delete records with zero volumes
    crud.market_depth.delete_many_sync({
        "symbol": order_in.symbol,
        "volume": 0
    })
    # Push actual data to sockets
    depth_all = {}
    for order_side in [TradeType.BUY, TradeType.SELL]:
        sort_by_price = -1 if order_side == TradeType.BUY else 1
        db_data = crud.market_depth.find_all_sync({
            "symbol": order_in.symbol,
            "volume": {"$gt": 0},
            "side": order_side,
        }, limit=30, order_by=[('price', sort_by_price)])
        depth_all[order_side.lower()] = db_data
        depth_all[f'total{order_side.capitalize()}'] = sum([row['volume'] for row in db_data])
        depth_all[f'max{order_side.capitalize()}'] = max([row['volume'] for row in db_data]) if db_data else 0

    if depth_all[TradeType.BUY.lower()] and depth_all[TradeType.SELL.lower()]:
        buy_price = depth_all[TradeType.BUY.lower()][0]['price']
        sell_price = depth_all[TradeType.SELL.lower()][0]['price']

        depth_all['spread'] = buy_price - sell_price
        depth_all['price'] = buy_price
    else:
        depth_all['spread'] = 0
        depth_all['price'] = 0

    mq.publisher.send_event("orderbook_event", depth_all, room=order_in.symbol)


def add_current_order_price(order: Order) -> dict:
    if order.side == TradeType.SELL:
        return {"current_ask": order.price}
    else:
        return {"current_bid": order.price}


def update_current_price(order: Order) -> dict:
    return crud.market.update_price_stat({"symbol": order.symbol},
                                         {'$set': add_current_order_price(order)})


def generate_market_stat(order: Order, market_state: dict) -> dict:
    last_trades = crud.trade.get_24_trades(symbol=order.symbol)
    price_24 = last_trades[0]['price'] if last_trades else order.price
    volume_24 = round(crud.order.get_volume_stat(symbol=order.symbol), 2)
    message = {
        "symbol": order.symbol,
        "current_ask": round(market_state['current_ask'], 2),
        "current_bid": round(market_state['current_bid'], 2),
        "last_change": market_state['last_change'],
        "market_accept_orders": market_state['market_accept_orders'],
        "price_24": round(Decimal(price_24), 2),
        "last_price": round(order.price, 2),
        "last_update_time": datetime.utcnow(),
        "volume_24": volume_24
    }
    return message


def push_market_ticker(order: Order, market_state: dict) -> None:
    message = generate_market_stat(order, market_state)
    crud.market.update_by_query_sync({"symbol": order.symbol}, {'$set': message})
    mq.publisher.send_event("ticker_event", message, room=order.symbol)


def update_quotes(sell_order: Order, trade_size: Decimal) -> dict:
    _ = background.send_message({
        'market_id': get_market_id_by_symbol(sell_order.symbol),
        'symbol': sell_order.symbol,
        'price': sell_order.price,
        'asset_amount': trade_size,
        'create_date': datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    }, settings.UPDATE_QUOTES_TASK, wait_result=False)
    return {'status': 'success'}


def change_balances(trade: Optional[Trade]) -> dict:
    return background.send_message(trade.json(), settings.CHANGE_BALANCE_TASK)


def process_market_deal(order: Order, trade: Trade) -> None:
    """  Push order_book, quotes, ticker events """

    update_market_depth(order)

    mq.publisher.send_event("trade_event", trade.dict(), room=trade.symbol)
    mq.publisher.send_event("change_order_status_event", order.dict())

    # Update current pair ask/bid
    market_state = update_current_price(order)

    push_market_ticker(order, market_state)
    _ = update_quotes(order, Decimal(trade.quantity))
