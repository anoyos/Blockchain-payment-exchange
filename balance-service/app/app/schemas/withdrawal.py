from datetime import datetime
from typing import List, Optional

from api_contrib.schemas.base import ResponseFormat
from pydantic import Field

from app.models.withdrawal import Withdrawal


class WithdrawalLegacy(Withdrawal):
    currency: Optional[str] = Field(description="DEPRECATED, use `asset_code` instead")
    currencyid: Optional[str] = Field(description="DEPRECATED. Use `asset_id` instead")
    date_requested: Optional[datetime] = Field(description="DEPRECATED. Use `transaction_time` instead")
    timestamp_execution: Optional[int] = Field(description="DEPRECATED. Use `applied_time` instead")
    txid: Optional[str] = Field(description="DEPRECATED. Use `tx_id` instead")
    withdrawalid: Optional[str] = Field(description="DEPRECATED. Use `id` instead")
    status: Optional[int] = 0

    def __init__(self, **data):
        super().__init__(**data)
        self.withdrawalid = self.id
        self.currencyid = self.asset_id
        self.currency = self.asset_code
        self.date_requested = self.transaction_time
        self.timestamp_execution = int(self.transaction_time.timestamp())
        self.txid = self.tx_id


class WithdrawalResponse(ResponseFormat):
    message: List[WithdrawalLegacy]
