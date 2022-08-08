from typing import Dict

from api_contrib.crud.base_mongo import CRUDBaseMongo
from pymongo import ReturnDocument
from decimal import Decimal


class CRUDMarket(CRUDBaseMongo):

    async def delete_one(self, query):
        await self.collection.delete_one(query)

    async def get_query_as_dict(self, query: Dict = None) -> Dict[str, Dict]:
        query_filter = query or {}
        result = {}
        cursor = self.collection.find(self.cast_id(query_filter)).sort([("last_price", 1)])
        async for row_item in cursor:
            item = self.cast_id(row_item)
            item['marketid'] = item['id']
            result[item['id']] = item
        return result

    def get_query_as_dict_sync(self, query: Dict = None) -> Dict[str, Dict]:
        query_filter = query or {}
        result = {}
        cursor = self.collection.find(self.cast_id(query_filter))
        for row_item in cursor:
            item = self.cast_id(row_item)
            item['marketid'] = item['id']
            result[item['id']] = item
        return result

    def update_price_stat(self, query: dict, data: dict):
        market = self.collection_sync.find_one(query)
        last_price = data['$set'].get('current_ask') or data['$set'].get('current_bid', 0)
        if int(market.get('last_price', 0)) == 0 or market.get('last_price') is None:
            last_change = 0
        else:
            last_change = round((last_price/Decimal(market['last_price']))*100, 2)-100

        data['$set'].update({"last_change": last_change})

        return self.collection_sync.find_one_and_update(
            query,
            data,
            return_document=ReturnDocument.AFTER
        )