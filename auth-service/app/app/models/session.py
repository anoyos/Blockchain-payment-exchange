from api_contrib.models.base import MongoDbModel

from app.models.base import CommonConfig


class Session(MongoDbModel):
    user_id: str
    status: str
    expires_at: str
    ip_address: str
    user_agent: str
    token: str
    refresh_token: str

    class Config(CommonConfig):
        collection_name = "session"

