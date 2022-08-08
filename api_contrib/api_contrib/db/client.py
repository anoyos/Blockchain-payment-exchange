from motor.motor_asyncio import AsyncIOMotorClient


class MongoDBClient(object):
    __instance = None

    def __new__(cls, settings) -> "MongoDBClient":
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
        return cls.__instance

    def __init__(self, settings):
        self.client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_STRING,
                                         maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
                                         minPoolSize=settings.MIN_CONNECTIONS_COUNT)

    def close_connection(self):
        self.client.close()




