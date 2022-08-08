from typing import Tuple

from redis import Redis

from app import models
from app.connections.redis import redis_connect
from app.market.core.queues import PriorityQueue


class OrderQueue(PriorityQueue):
    def push(self, order: models.Order):
        return NotImplementedError


class SellQueue(OrderQueue):

    def __init__(self, market_id: str, redis_client: Redis):
        self.key = f'sell_{market_id}'
        super().__init__(redis_client, self.key)

    def push(self, order: models.Order):
        self.add({order.id: float(order.price)})


class BuyQueue(OrderQueue):

    def __init__(self, market_id: str, redis_client: Redis):
        self.key = f'buy_{market_id}'
        super().__init__(redis_client, self.key)

    def push(self, order: models.Order):
        self.add({order.id: -1 * float(order.price)})


class MarketOrderDepth:
    def __init__(self, market: models.Market):
        self.market = market
        self.redis_client = redis_connect
        self.buy_queue = BuyQueue(self.market.id, redis_client=self.redis_client)
        self.sell_queue = SellQueue(self.market.id, redis_client=self.redis_client)

    def get_queue(self, order_side: str) -> OrderQueue:
        return self.buy_queue if order_side == models.TradeType.BUY else self.sell_queue

    def get_first_by_side(self, side: str) -> Tuple[bytes, float]:
        queue = self.get_queue(side)
        # logger.info(f"{self.market.market_name} {side} queue size: {queue.size()}")
        first_order = queue.first()
        return first_order[0] if first_order else (b'', 0.0)

    def delete(self, order: models.Order) -> None:
        queue = self.get_queue(order.side)
        queue.delete(order.id)

    def push(self, order: models.Order) -> None:
        queue = self.get_queue(order.side)
        queue.push(order)
