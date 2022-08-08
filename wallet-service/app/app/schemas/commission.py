from decimal import Decimal
from typing import Optional

from api_contrib.models import description
from api_contrib.schemas.base import ResponseFormat
from pydantic import BaseModel, Field


class CommissionScheme(BaseModel):
    estimated_fee: Decimal = Field(description="Commission optimal for send transaction")


class CommissionRequest(BaseModel):
    asset_id: Optional[str] = Field(description=description.ASSET_ID)
    address: Optional[str] = Field(description="Address to Withdrawal receive")
    amount: Optional[str] = Field(description="Amount of Withdrawal units")


class CommissionResponse(ResponseFormat):
    message: CommissionScheme
