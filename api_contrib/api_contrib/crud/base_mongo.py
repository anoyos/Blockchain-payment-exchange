from typing import Dict, List, TypeVar, Any, Type


ModelType = TypeVar("ModelType")


class CRUDBaseMongo:
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**
        * `database_name`: Mongo database name
        * `db_collection`: Mongo collection name

        """
        self.collection_name = model.Config.collection_name
        self.database_name = model.Config.database_name
        self.model = model
        client = self.model.Config.db_client
        self.collection = client[self.database_name][self.collection_name]

    @staticmethod
    def replace_id(item: Dict) -> Dict:
        """ For success pydantic  validation
            replace private _id: ObjectId  in input dict for
            id: str in output
        """
        item['id'] = str(item.pop(['_id']))
        return item

    async def find_all(self) -> List[Dict]:
        return [item async for item in self.collection.find()]

    async def get_query_as_dict(self, query: Dict = None) -> Dict[str, Dict]:

        query_filter = query or {}
        return dict([
            (str(item['_id']), self.replace_id(item)) async for item in self.collection.find(query_filter)
        ])

    async def find_one(self, query: dict) -> Dict:
        row = await self.collection.find_one(query)
        return self.replace_id(row)

    async def insert_one(self, obj_in) -> Any:
        x = obj_in.dict()
        result = await self.collection.insert_one(x)
        id = str(result.inserted_id)
        return id
