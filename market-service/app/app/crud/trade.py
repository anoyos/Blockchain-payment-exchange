from datetime import datetime, timedelta
from typing import Dict, List

from api_contrib.crud.base_mongo import CRUDBaseMongo


class CRUDTrade(CRUDBaseMongo):

    def get_24_trades(self, symbol: str) -> List[Dict]:
        cursor = self.collection_sync.find({
            "symbol": symbol,
            "create_date": {"$gt": datetime.now() - timedelta(days=1)}
        }, limit=1).sort([("create_date", 1)])

        return [row for row in cursor]
