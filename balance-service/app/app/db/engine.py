from api_contrib.db.client import MongoDBClient, MongoDBClientSync
from app.core.config import settings

client = MongoDBClient(settings).client
client_sync = MongoDBClientSync(settings).client

