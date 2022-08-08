from decimal import Decimal
from typing import List

from api_contrib.crud.base_mongo import CRUDBaseMongo
from bson.objectid import ObjectId


class CRUDEntry(CRUDBaseMongo):

    def push_item(self, query: dict, item: dict):

        entry = self.get_or_create_sync(query)
        # if
        self.collection_sync.update_one({'_id': ObjectId(entry['id'])},
                                        {'$push': {"items": item}})

    async def summary_report(self, accounts: List[str]) -> dict:
        """
        Total:
        ---------
        report['BTC']['commission'] = 100
        report['BTC']['deposits'] = 200
        report['BTC']['withdrawal'] = 5

        Daily:
        ---------
        report['BTC'][2020-01-01]['commission'] = 100
        report['BTC'][2020-01-01]['deposits'] = 200
        report['BTC'][2020-01-01]['withdrawal'] = 50
        """
        report = {}

        data = await self.find_all({"account_id": {"$in": accounts}})

        for row in data:
            # _asset = row['asset_code']
            _time = row['event_date']
            _type = row['event_type']

            # if _asset not in report:
            #     report[_asset] = {}
            if _time not in report:
                report[_time] = {}
            if _type not in report[_time]:
                report[_time][_type] = Decimal(0)

            for item in row['items']:
                report[_time][_type] = Decimal(item['increment']) + Decimal(report[_time][_type])

        return report
