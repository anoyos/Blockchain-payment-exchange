from decimal import Decimal
from os import getenv

from api_contrib.core.config import Settings
from pydantic import AnyUrl


class AppSettings(Settings):
    """ Rewrite project specific settings here """
    ORDERS_FEE: float = getenv('ORDERS_FEE', default=0.002)
    REDIS_URL: str = getenv('REDIS_URL')
    REDIS_PASS: str = getenv('REDIS_PASS')
    CELERY_BROKER_URL: str = getenv('CELERY_BROKER_URL')
    CELERY_BACKEND_URL: str = getenv('CELERY_BACKEND_URL')
    CHANGE_BALANCE_TASK: str = getenv('CHANGE_BALANCE_TASK', default='app.worker.apply_trade')
    UPDATE_QUOTES_TASK: str = getenv('UPDATE_QUOTES_TASK', default='app.quotes_worker.update_quotes')
    COMMISSION_PERCENT: Decimal = getenv('COMMISSION_PERCENT', default=Decimal('0.002'))
    PROJECT_NAME: str = getenv('PROJECT_NAME', 'market-service')
    API_V1_STR: str = getenv('API_V1_STR', '/api/v1/market')
    QUOTES_SERVICE_URL: str = getenv('QUOTES_SERVICE_URL')
    CLUSTER_API_KEY: str = getenv('CLUSTER_API_KEY')
    STAT_API_URL: AnyUrl = getenv('STAT_API_URL', default='https://api.coingecko.com/api/v3/coins/markets')
    LIQUIDITY_RESERVE_CONSTANT: Decimal = getenv('LIQUIDITY_RESERVE_CONSTANT', Decimal(0.5))
    B2BX_URL: AnyUrl = getenv('B2BX_URL', default='https://b2t-api-b2bx.flexprotect.org')


settings = AppSettings()
