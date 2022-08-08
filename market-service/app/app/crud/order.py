from datetime import datetime, timedelta
from typing import Dict, List, Type, Any, Union

from api_contrib.crud.base_mongo import CRUDBaseMongo, ModelType
from bson.objectid import ObjectId

from app.models.order import OrderStatus, Order


class CRUDOrder(CRUDBaseMongo):

    async def find_id_in(self, values: List = None) -> Any:
        cursor = self.collection.find(
            {"_id": {"$in": [ObjectId(v) for v in values]}}
        )
        return [self.cast_id(row_item)
                async for row_item in cursor]

    def find_id_in_sync(self, values: List = None) -> List[Dict]:
        cursor = self.collection_sync.find(
            {"_id": {"$in": [ObjectId(v) for v in values]}}
        )
        return [self.cast_id(row_item) for row_item in cursor]

    def update_by_kwargs(self, order: Order, **kwargs) -> None:
        self.update_obj_sync(order, kwargs)

    def find_by_id_sync(self, obj_id: str, return_obj=True) -> Union[Type[ModelType], Dict]:
        row = self.collection_sync.find_one({"_id": ObjectId(obj_id)})
        cast_row = self.cast_id(row)
        return self.model(**cast_row) if return_obj else cast_row

    def get_volume_stat(self, symbol: str):
        data = self.collection_sync.aggregate([
            {
                "$match": {
                    "symbol": symbol,
                    "status": OrderStatus.EXECUTED,
                    "create_date": {"$gt": datetime.now() - timedelta(days=1)}
                }
            },
            {
                "$group":
                    {"_id": "$cust_id",
                     "total": {"$sum": "$quantity"}
                     }
            },
        ])
        x = [i for i in data]
        return x[0]['total'] if x else 0
