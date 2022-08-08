from api_contrib.crud.base_mongo import CRUDBaseMongo


class CRUDDeposit(CRUDBaseMongo):

    def save_address_for_user(self, query: dict):
        user_id_filter = {
            'user_id': query.pop('user_id')
        }
        # get record without user_id
        db_obj = self.find_one_sync(query=query)

        # if address found but doesn't link with any user - assign it to user
        if db_obj:
            self.update_sync(db_obj, user_id_filter)

        # create new record with user_id
        else:
            query.update(user_id_filter)
            return self.insert_one_sync(self.model(**query))

    def get_free_address(self, asset_code) -> str:
        query_filter = {"user_id": None, "asset_code": asset_code}

        data = [self.cast_id(item)
                for item in
                self.collection_sync.find(query_filter, limit=1).sort([("mapping_num", 1)])
                ]
        return data[0]['address']
