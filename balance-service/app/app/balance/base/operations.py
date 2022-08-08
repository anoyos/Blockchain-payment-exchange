import json
from datetime import datetime

from api_contrib.core.utils import CustomEncoder, logger

from app import crud
from app.api.internal.mq_publisher import publisher


def increment_account_balance(account: dict,
                              increment: dict,
                              event_type: str = None,
                              event_id: str = None,
                              push_entry: bool = True):
    if increment.get('balance', 0) == 0 and increment.get('available', 0) == 0:
        return

    doc = crud.balance.increment(account, increment)
    # logger.info("send balance_change_event")
    publisher.publish(bytes(json.dumps({
        "event_name": "balance_change_event",
        "data": {
            "user_id": doc["user_id"],
            "asset_code": doc["asset_code"],
            "balance": doc["balance"],
            "available": doc["available"],
            "locked": doc["locked"]
        }},
        cls=CustomEncoder), "utf-8"))

    if push_entry:
        crud.entry.push_item(query={
            "event_date": datetime.now().date().isoformat(),
            "event_type": event_type,
            "asset_code": account['asset_code'],
            "account_id": account['id'],
        },
            item={
                "event_id": event_id,
                "event_time": datetime.now(),
                "event_type": event_type,
                "increment": increment['balance'],
                "balance_before": account['balance'],
                "balance_after": doc['balance'],
            })
