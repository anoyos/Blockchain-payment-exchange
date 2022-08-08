import json
from typing import Any
from api_contrib.core.utils import CustomEncoder
from pydantic import BaseModel
from decimal import Decimal
from .base import ResponseFormat


class BackgroundMessage(BaseModel):
    @property
    def celery_msg_name(self):
        raise NotImplemented


class CeleryMessage:

    def __init__(self, model: BackgroundMessage, celery_app: Any):
        self.model = model
        self.celery_app = celery_app

    def send(self, return_result=True):
        data = json.dumps(self.model.dict(), cls=CustomEncoder)
        task_name = self.model.celery_msg_name()
        async_task_promise = self.celery_app.send_task(task_name, args=[data])
        if return_result:
            task_result = async_task_promise.get()
            return ResponseFormat(**task_result)
        else:
            return ResponseFormat(message={})


class LockBalancePayload(BackgroundMessage):
    user_id: str
    amount: Decimal
    asset_id: str

    def celery_msg_name(self):
        return 'app.worker.lock_balance'

