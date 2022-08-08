from typing import Dict

from api_contrib.crud.base_mongo import CRUDBaseMongo


class CRUDAsset(CRUDBaseMongo):

    async def get_query_as_dict(self, query: Dict = None) -> Dict[str, Dict]:
        query_filter = query or {}
        result = {}
        cursor = self.collection.find(self.cast_id(query_filter))
        async for row_item in cursor:
            item = self.cast_id(row_item)
            front_id = item['asset_id']
            item['id'] = front_id
            result[front_id] = item
        return result

    def get_query_as_dict_sync(self, query: Dict = None) -> Dict[str, Dict]:
        query_filter = query or {}
        result = {}
        cursor = self.collection_sync.find(self.cast_id(query_filter))
        for row_item in cursor:
            item = self.cast_id(row_item)
            front_id = item['asset_id']
            item['id'] = front_id
            result[front_id] = item
        return result
