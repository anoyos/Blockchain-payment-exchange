from prometheus_client.exposition import start_http_server

from app.core.connector import celery_app
from app.core.config import settings
from app.blockchain.handlers.ethereum.background import process_withdrawal_transaction

if settings.IS_CELERY_WORKER:
    start_http_server(80)


@celery_app.task()
def apply_withdrawal_transaction(message):
    return process_withdrawal_transaction(message)

