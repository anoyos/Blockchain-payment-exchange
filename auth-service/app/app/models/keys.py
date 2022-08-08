from api_contrib.models.base import MongoDbModel

from app.models.base import CommonConfig


class ApiKey(MongoDbModel):
    user_id: str
    secret: str
    status: str = 'ACTIVE'

    class Config(CommonConfig):
        collection_name = "api_keys"

