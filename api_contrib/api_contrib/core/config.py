from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from os import getenv


class Settings(BaseSettings):
    API_V1_STR: str = getenv('API_V1_STR')
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = getenv('BACKEND_CORS_ORIGINS', [])

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = getenv('PROJECT_NAME')

    # MongoDB connection
    MONGODB_URL: str = getenv('MONGODB_URL')
    MONGODB_USER: str = getenv('MONGODB_USER')
    MONGODB_ROOT_PASSWORD: str = getenv('MONGODB_ROOT_PASSWORD')
    MONGODB_PASSWORD: str = getenv('MONGODB_PASSWORD')
    MONGODB_NAME: str = getenv('MONGODB_NAME')
    cred = f"{MONGODB_USER}:{MONGODB_PASSWORD}"
    MONGODB_CONNECTION_STRING = f'mongodb://{cred}@{MONGODB_URL}/?authSource={MONGODB_NAME}'

    if getenv('USE_REPLICA_SET'):
        MONGODB_CONNECTION_STRING = MONGODB_CONNECTION_STRING + '&replicaSet=rs0'

    MIN_CONNECTIONS_COUNT: int = getenv('MIN_CONNECTIONS_COUNT', 0)
    MAX_CONNECTIONS_COUNT: int = getenv('MAX_CONNECTIONS_COUNT', 100)

    MARKET_COLLECTION: str = 'markets_collection'
    ASSET_COLLECTION: str = 'assets_collection'


settings = Settings()
