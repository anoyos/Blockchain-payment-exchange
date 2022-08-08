from api_contrib.crud.base_mongo import CRUDBaseMongo
from api_contrib.models.base import MongoDbModel
from bson.objectid import ObjectId


class CRUDTransaction(CRUDBaseMongo):

    async def set_status(self, obj: MongoDbModel, status: str) -> None:
        await self.collection.update_one({'_id': ObjectId(obj.id)},
                                         {'$set': {
                                             "status": status
                                         }})

    def find_min(self, asset_code: str) -> dict:
        data = self.collection_sync.aggregate([
            {
                "$match": {
                    "asset_code": asset_code
                }
            },
            {
                "$group":
                    {"_id": "$address",
                     "min_value": {"$min": "$amount"}
                     }
            },
        ])
        x = [i for i in data]
        from app.core.constants import SERVICE_BTC_ADDRESS
        return x[0] if x else {"min_value": 1.0, "_id": SERVICE_BTC_ADDRESS}


class CRUDBlocks(CRUDBaseMongo):
    def get_or_create(self, query, obj_data: dict = None):
        db_obj = self.find_one_sync(query=query)
        if db_obj:
            return db_obj
        else:
            return self.create_sync(query, return_obj=True)


class CRUDAccount(CRUDBaseMongo):

    def update_after_withdrawal(self, obj, balance):
        self.collection_sync.update_one(
            {'_id': ObjectId(obj.id)},
            {
                '$inc': {"withdrawal_count": 1},
                '$set': {"balance": balance}
            }
        )