from os import getenv

from api_contrib.core.config import Settings
from pydantic import AnyHttpUrl


class AppSettings(Settings):
    AUTH_METHOD: str = getenv('AUTH_METHOD', default='/login/')
    MARKET_SERVICE_URL: str = getenv('MARKET_SERVICE_URL')
    AUTH_SERVICE_URL: str = getenv('AUTH_SERVICE_URL')
    AUTH_SERVICE_URL_EXT: str = getenv('AUTH_SERVICE_URL_EXT', default=AUTH_SERVICE_URL)
    BALANCE_SERVICE_URL: str = getenv('BALANCE_SERVICE_URL')
    BITCOINLIB_DB_URL: str = getenv('BITCOINLIB_DB_URL')
    CELERY_BROKER_URL: str = getenv('CELERY_BROKER_URL')
    CELERY_BACKEND_URL: str = getenv('CELERY_BACKEND_URL')
    PROJECT_NAME: str = getenv('PROJECT_NAME', 'wallet-service')
    API_V1_STR: str = getenv('API_V1_STR', '/api/v1/currency')
    IS_CELERY_WORKER: bool = getenv('IS_CELERY_WORKER', False)


class ChainSetting:
    RPC_URL: str
    FACTORY_CONTRACT_ABI_PATH: str
    FACTORY_CONTRACT_ADDRESS: str
    FACTORY_OWNER_KEY: str
    RECEIVERS_BATCH_SIZE: int

    def __init__(self, chain_code: str):
        self.RPC_URL: str = getenv(f'RPC_URL_{chain_code}')
        self.FACTORY_CONTRACT_ABI_PATH: str = getenv(f'FACTORY_CONTRACT_ABI_PATH_{chain_code}')
        self.FACTORY_CONTRACT_ADDRESS: str = getenv(f'FACTORY_CONTRACT_ADDRESS_{chain_code}')
        self.FACTORY_OWNER_KEY: str = getenv(f'FACTORY_OWNER_KEY_{chain_code}')
        self.RECEIVERS_BATCH_SIZE: int = getenv(f'RECEIVERS_BATCH_SIZE{chain_code}', default=5)


settings = AppSettings()
