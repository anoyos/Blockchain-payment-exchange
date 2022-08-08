from typing import Dict, List
from typing import Type

from api_contrib.crud.base_mongo import CRUDBaseMongo
from api_contrib.crud.base_mongo import ModelType
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from app.core import contants
from app.models.balance import BalanceSettings


class CRUDBalance(CRUDBaseMongo):

    def __init__(self, model: Type[ModelType]):
        """
        Extend base class with sync methods, for use with not thread-safe frameworks, e.g Celery
        """
        super().__init__(model)
        client_sync = self.model.Config.db_client_sync

    def create_or_update(self, obj: Dict, key_fields: List[str]) -> None:
        db_obj = self.find_one_sync(query=dict(
            (k, obj[k]) for k in key_fields
        ))
        if db_obj:
            self.collection.update_one({'_id': ObjectId(db_obj['id'])},
                                       {'$inc':
                                            {'balance': obj['balance']}
                                        })

            balance_id = db_obj['id']
        else:
            d = self.model(**obj)
            balance_id = self.insert_one_sync(d)

        return balance_id

    def update_sync_by_query(self, query: dict, values: dict) -> None:
        self.collection_sync.update_one(query, values)

    def increment(self, account: dict, increment: dict):
        return self.cast_id(self.collection_sync.find_one_and_update(
            {"_id": ObjectId(account['id'])},
            {"$inc": increment}
            , return_document=ReturnDocument.AFTER
        ))

    async def get_or_create_user_balances(self, query: Dict) -> List[Dict]:

        balances = await self.find_all(query={
            'user_id': query['user_id']
        })

        user_assets = [account['asset_id'] for account in balances]

        for system_asset_id, system_asset in contants.assets.items():
            if system_asset_id not in user_assets:
                await self.create({
                    'user_id': query['user_id'],
                    'asset_id': system_asset_id,
                    'asset_code': system_asset['short_name'],
                    'settings': BalanceSettings(withdrawal_enabled=system_asset.get('withdrawal_enabled', False))
                })

        return await self.find_all(query={
            'user_id': query['user_id']
        })
