from api_contrib.core.config import Settings
from os import getenv


class AppSettings(Settings):
    AUTH_METHOD: str = getenv('AUTH_METHOD', default='/login/')
    MARKET_SERVICE_URL: str = getenv('MARKET_SERVICE_URL')
    AUTH_SERVICE_URL: str = getenv('AUTH_SERVICE_URL')
    AUTH_SERVICE_URL_EXT: str = getenv('AUTH_SERVICE_URL_EXT', default=AUTH_SERVICE_URL)
    CELERY_BROKER_URL: str = getenv('CELERY_BROKER_URL')
    CELERY_BACKEND_URL: str = getenv('CELERY_BACKEND_URL')
    ASSET_INTERNAL_SOURCE: str = getenv('ASSET_INTERNAL_SOURCE', default='app.worker.get_assets')
    IS_CELERY_WORKER: bool = bool(getenv('IS_CELERY_WORKER'))
    ASSET_CONFIG_PATH:  str = getenv('ASSET_CONFIG_PATH')
    PROJECT_NAME: str = getenv('PROJECT_NAME', 'balance-service')
    API_V1_STR: str = getenv('API_V1_STR', '/api/v1/balance')
    TOTAL_BALANCE_CURRENCY: str = getenv('TOTAL_BALANCE_CURRENCY', 'tUSDT')


settings = AppSettings()
