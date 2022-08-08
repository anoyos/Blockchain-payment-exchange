from api_contrib.crud.base_mongo import CRUDBaseMongo


class CRUDSession(CRUDBaseMongo):

    async def update_many(self, query: dict, values: dict):
        await self.collection.update_many(query,
                                          {'$set': values})
