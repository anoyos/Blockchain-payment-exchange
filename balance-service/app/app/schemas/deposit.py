from datetime import datetime
from typing import List, Optional

from api_contrib.schemas.base import ResponseFormat
from pydantic import Field

from app.models.deposit import Deposit


class DepositLegacy(Deposit):
    currencyid: Optional[str] = Field(description="DEPRECATED. USE asset_id instead")
    date_requested: Optional[int] = Field(description="DEPRECATED. USE transaction_time instead")
    txid: Optional[str] = Field(description="DEPRECATED. USE tx_id instead")
    timestamp_execution: Optional[int] = Field(description="DEPRECATED. USE applied_time instead")
    confirmations: Optional[int] = Field(description="Not implemented yet", default=1)
    confirmations_needed: Optional[int] = Field(description="Not implemented yet", default=6)
    deposit_date: Optional[int] = Field(description="Not implemented yet")
    confirmed: Optional[bool] = Field(description="Not implemented yet", default=True)
    accounted: Optional[bool] = Field(description="Not implemented yet", default=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.currencyid = self.asset_id
        self.date_requested = int(self.transaction_time.timestamp())
        self.txid = self.txid
        self.timestamp_execution = int(self.transaction_time.timestamp())
        self.deposit_date = int(self.transaction_time.timestamp())


class DepositResponse(ResponseFormat):
    message: List[DepositLegacy]

    class Config:
        arbitrary_types_allowed = True
