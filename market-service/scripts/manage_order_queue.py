from app.market.core.depth import MarketOrderDepth
from bson import ObjectId

from app.core import constants
from app.models import Market


def time_from_id(row_id):
    _id = row_id.decode()
    return ObjectId(_id).generation_time.strftime('%Y-%m-%d %H:%M:%S')


def clear_all():
    """ Need to patch redis config to turn on this command """
    from redis import Redis

    from app.core.config import settings

    client = Redis(host=settings.REDIS_URL, password=settings.REDIS_PASS)

    client.flushall()


def clear_queue(market: Market):
    market_depth = MarketOrderDepth(market)
    print(f"clear queues for {market_depth.market.symbol}")
    print(f"sell size: {market_depth.sell_queue.size()}")
    print(f"buy size: {market_depth.sell_queue.size()}")

    for queue in [market_depth.sell_queue, market_depth.buy_queue]:
        queue_len = queue.size()
        while queue_len > 0:
            order_id = queue.pop()
            queue_len = queue.size()
            print(f"drop order {order_id}, que_len: {queue_len}")

    print(f"sell size: {market_depth.sell_queue.size()}")
    print(f"buy size: {market_depth.buy_queue.size()}")


def list_queues(market: Market) -> None:
    market_depth = MarketOrderDepth(market)

    fist_order, score_first = market_depth.buy_queue.first()[0]
    last_order, score_last = market_depth.buy_queue.last()[0]

    print(f"first: {score_first:.8f} time: {time_from_id(fist_order)}")
    print(f" last: {score_last:.8f}  time: {time_from_id(last_order)}")
    print(f"sell size: {market_depth.sell_queue.size()}")
    print(f"buy size: {market_depth.buy_queue.size()}")


if __name__ == '__main__':
    for market_obj in constants.ALL_MARKETS:
        clear_queue(market_obj)
