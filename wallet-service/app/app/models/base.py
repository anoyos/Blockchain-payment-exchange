from app.core.config import settings
from app.db.engine import client_sync, client


class CommonConfig:
    database_name = settings.MONGODB_NAME
    db_client = client
    db_client_sync = client_sync
