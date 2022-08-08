from decimal import Decimal
from typing import Optional

from api_contrib.models import base, description
from pydantic import Field

from .base import CommonConfig


class LastReadBlock(base.MongoDbModel):
    asset_code: str = Field(description=description.ASSET_CODE)
    last_read_block_num: int = Field(description=description.ASSET_CODE, default=0)

    class Config(CommonConfig):
        collection_name = "last_read_blocks"


class SystemAccount(base.MongoDbModel):
    asset_code: str
    address: str
    balance: Optional[Decimal] = 0
    deposit_count: Optional[int] = 0
    withdrawal_count: Optional[int] = 0

    class Config(CommonConfig):
        collection_name = "system_accounts"


class UserContracts(base.MongoDbModel):
    asset_code: str
    address: str
    mapping_num: int
    user_id: Optional[str] = None
    balance: Optional[Decimal] = 0

    class Config(CommonConfig):
        collection_name = "user_contracts"
