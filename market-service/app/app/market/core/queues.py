from typing import Mapping

from redis import Redis


class PriorityQueue:
    """
    Redis-based priority queue, based on following explanation
    https://programmersought.com/article/9243985546/

    Sorted set
    Sorted set is a type of data structure provided by Redis that combines the characteristics of set and hash.
    First, each element in the sorted set is unique; second, each element in the sorted set is associated with a
     floating point value (called a score). In addition to this, the elements in the sorted set are ordered,
     and these elements are sorted according to the following rules:

    If A and B are two elements with different scores, then A > B if and only if A.score > B.score
    If A and B have the same score, then A > B if and only if the lexicographic order of A is greater than B

    In this implementation
        1) score == price for sell orders
                    -1 * price for buy orders
        2) Key = Mongo ObjectId
        https://docs.mongodb.com/manual/reference/method/ObjectId/#ObjectIDs-BSONObjectIDSpecification)
        based on Timestamp, so older ObjectId lexicographically bigger than younger ObjectId

        In this case nearest order for processing will be on the left side of array.

    1) With the same price first added ObjectId will be first(),
    because hex-encoded timestamp 606eccbc less than 606eccbd

    > queue.add({"606eccbc7d740c72b32da30b": 11}, "")
    1
    > queue.add({"606eccbd7d740c72b32da310": 11}, "")
    1
    > queue.first()
    [(b'606eccbc7d740c72b32da30b', 11.0)]

    2) Order will lowest price will be first ("best price" rule)
    > queue.add({"606eccbd7d740c72b32da315": 10}, "")
    1
    > queue.first()
    [(b'606eccbd7d740c72b32da315', 10.0)]

    3) SELL orders priority
    > queue.client.zrange(queue.key,0, -1, withscores=True)
    [(b'606eccbd7d740c72b32da315', 10.0), (b'606eccbc7d740c72b32da30b', 11.0), (b'606eccbd7d740c72b32da310', 11.0)]

    4)  BUY orders priority
    > queue.client.zrange(queue.key,0, -1, withscores=True)
    [(b'606eccbc7d740c72b32da30b', -11.0), (b'606eccbd7d740c72b32da310', -11.0), (b'606eccbd7d740c72b32da315', -10.0)]

    *For BUY orders we revert score based on price with -1
    So, that biggest price will be with lowest score and place in left side of array

    5) lexicographically compare ObjectId
    > '606eccbd7d740c72b32da310' > '606eccbc7d740c72b32da30b'
    True

    """

    def __init__(self, redis_client: Redis, key):
        self.client = redis_client
        self.key = key

    def add(self, score_pair: Mapping):
        return self.client.zadd(self.key, score_pair, nx=True)

    def first(self):
        return self.client.zrange(self.key, 0, 0, withscores=True)

    def range(self):
        return self.client.zrange(self.key, 0, -1, withscores=True)

    def rev_range(self):
        return self.client.zrevrange(self.key, 0, -1, withscores=True)

    def last(self):
        return self.client.zrevrange(self.key, 0, 0, withscores=True)

    def all(self):
        return [item.decode() for item in
                self.client.zrange(self.key, 0, -1, withscores=False)]

    def delete(self, order_id: str):
        return self.client.zrem(self.key, order_id)

    def size(self):
        return self.client.zcount(self.key, '-inf', '+inf')

    def pop(self):
        """ Note: This method is not thread safe """
        score = None
        member = None
        result = self.first()
        if result:
            member, score = result[0]
            ret = self.client.zrem(self.key, member)
            assert ret == 1
        return member, score

    def card(self):
        return self.client.zcard(self.key)

    def __repr__(self):
        return f"PriorityQueue: {self.key}"
