from decimal import Decimal

from api_contrib.models import description
from api_contrib.models.base import MongoDbModel
from pydantic import Field, BaseModel
from typing import Optional
from .base import CommonConfig


class AccountTypes:
    REGULAR = "REGULAR"
    PROFIT = "PROFIT"
    SPEND = "SPEND"


class BalanceSettings(BaseModel):
    deposit_enabled: bool = True
    withdrawal_enabled: bool = True
    confirmations: int = 3
    has_withdrawallimit: bool = False
    is_delisted: bool = False
    txfee: float = 0.0
    will_be_delisted: bool = False


class Balance(MongoDbModel):
    user_id: str = Field(description=description.USER_ID)
    asset_id: str = Field(description=description.ASSET_ID)
    asset_code: str = Field(description=description.ASSET_CODE)
    balance: Decimal = Field(description="User unique identifier", default=Decimal(0))
    available: Decimal = Field(description="User unique identifier", default=Decimal(0))
    locked: Decimal = Field(description="User unique identifier", default=Decimal(0))
    settings: dict = Field(description="Use for settings for web-app", default=BalanceSettings().dict())
    account_type: Optional[str] = Field(description="Purpose of account's usage", default=AccountTypes.REGULAR)

    class Config(CommonConfig):
        collection_name = "accounts"
