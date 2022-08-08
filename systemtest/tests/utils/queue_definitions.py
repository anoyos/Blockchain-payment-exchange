import os

from kombu import Exchange, Queue


def make_queue(exchange_name, queue_name, exchange_durable=False, queues_durable=False):
    exchange = Exchange(exchange_name, durable=exchange_durable)
    queue = Queue(queue_name, exchange, durable=queues_durable)
    return queue


app_conf = os.environ.get("APP_CONFIG")

BALANCE_QUEUE = make_queue("systemtest-balance-exchange", "systemtest-balance-queue")
BLOCK_CHAIN_ROUTER_QUEUE = make_queue("systemtest-blockchain_router-exchange", "systemtest-blockchain_router-queue")
MARKET_QUEUE = make_queue("systemtest-market-exchange", "systemtest-market-queue")
TOKEN_QUEUE = make_queue("systemtest-token-exchange", "systemtest-token-queue")
WALLET_QUEUE = make_queue("systemtest-wallet-exchange", "systemtest-wallet-queue")
