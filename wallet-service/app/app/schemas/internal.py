import json

from api_contrib.core.utils import CustomEncoder
from pydantic import BaseModel

from app import schemas
from app.core.connector import celery_app
from app.models import wallet, base


class ForwardedMessage(BaseModel):

    @property
    def celery_msg_name(self):
        raise NotImplemented

    def send(self, return_result=True):
        data = json.dumps(self.dict(), cls=CustomEncoder)
        task_name = self.celery_msg_name()
        async_task_promise = celery_app.send_task(task_name, args=[data])
        if return_result:
            task_result = async_task_promise.get()
            return schemas.ResponseFormat(**task_result)
        else:
            return schemas.ResponseFormat(message={})


class LockBalanceMessage(schemas.WithdrawalRequest, ForwardedMessage):

    def celery_msg_name(self):
        return 'app.worker.lock_balance'


class ApplyTransactionMessage(wallet.Transaction, ForwardedMessage):
    def celery_msg_name(self):
        return 'app.worker.apply_blockchain_transaction'


class ApplyWithdrawalMessage(ForwardedMessage):
    tx_id: str
    asset_code: str

    def celery_msg_name(self):
        return 'app.worker.apply_withdrawal_transaction'
