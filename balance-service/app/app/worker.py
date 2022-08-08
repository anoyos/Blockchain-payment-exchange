from prometheus_client.exposition import start_http_server

from app.api.internal.celery import celery_app
from app.api.internal.tools import process
from app.balance import transaction, trade, lock
from app.core.config import settings

if settings.IS_CELERY_WORKER:
    start_http_server(80)


@celery_app.task()
def apply_blockchain_transaction(message):
    return process(transaction.apply, message)


@celery_app.task()
def apply_trade(message):
    return process(trade.apply, message)


@celery_app.task()
def lock_balance(message):
    return process(lock.apply, message)
