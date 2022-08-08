from api_contrib.schemas.base import ResponseFormat
from api_contrib.models import description
from pydantic import BaseModel, Field
from typing import Optional
from app.models.wallet import Transaction


class WithdrawalScheme(Transaction):
    pass


class WithdrawalRequest(BaseModel):
    user_id: Optional[str] = Field(description=description.USER_ID)
    asset_id: Optional[str] = Field(description=description.ASSET_ID)
    asset_code: Optional[str] = Field(description=description.ASSET_CODE)
    amount: str = Field(description="withdrawal amount user requested")
    address: str = Field(description="address amount user requested")
    commission: Optional[str] = Field(description="Estimated fee for transaction")
    mfa_code: Optional[int] = Field(description="code from google authenticator")


class WithdrawalResponse(ResponseFormat):
    message: str = "OK"
