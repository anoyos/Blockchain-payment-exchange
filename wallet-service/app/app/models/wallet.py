from datetime import datetime
from decimal import Decimal
from typing import Optional

from api_contrib.models import base, description
from pydantic import Field

from app.core.constants import AddressStatus
from .base import CommonConfig


class Wallet(base.MongoDbModel):
    currency_id: str = Field(description=description.BASE_CURRENCY_ID)

    class Config(CommonConfig):
        collection_name = "wallets"


class ProcessedTransaction(base.MongoDbModel):
    wallet_id: int = Field(description="Wallet unique identifier")
    tran_id: int = Field(description="Last transaction id processed for wallet")

    class Config(CommonConfig):
        collection_name = "processed_transaction"


class DepositAddresses(base.MongoDbModel):
    user_id: Optional[str] = Field(description=description.USER_ID)
    address: str = Field(description="Address of generated for user to deposit")
    create_date: datetime = Field(description="Datetime of record creation", default_factory=datetime.now)
    status: str = Field(description="Status of address usage: USED/UNUSED", default=AddressStatus.UNUSED)
    currency_name: str = Field(description=description.BASE_CURRENCY_CODE)
    asset_id: str = Field(description=description.ASSET_ID)
    asset_code: Optional[str] = Field(description=description.ASSET_CODE)
    mapping_num: Optional[int] = Field(description="Mapping index in smart contract for ERC20 tokens")
    balance: Optional[Decimal] = 0

    class Config(CommonConfig):
        collection_name = "deposit_addresses_pool"


class TransactionIn(base.MongoDbModel):
    user_id: str = Field(description=description.USER_ID)
    address: str = Field(description="Address of generated for user to deposit")
    create_date: datetime = Field(description="Datetime of record creation", default_factory=datetime.now)
    status: str = Field(description="Status of address usage: USED/UNUSED", default=AddressStatus.UNUSED)
    currency_name: str = Field(description=description.BASE_CURRENCY_CODE)
    asset_id: str = Field(description=description.ASSET_ID)
    asset_code: Optional[str] = Field(description=description.ASSET_CODE)

    class Config(CommonConfig):
        collection_name = "transactions"


class TransactionStatus:
    NEW = "NEW"
    IN_PROCESS = "IN_PROCESS"
    DONE = "DONE"
    ERROR = "ERROR"


class Transaction(base.MongoDbModel):
    user_id: str = Field(description=description.USER_ID)
    address: str = Field(description="Address of generated for user to withdrawal")
    create_date: datetime = Field(description="Datetime of record creation", default_factory=datetime.now)
    status: str = Field(description="Status of transaction", default=TransactionStatus.NEW)
    asset_id: str = Field(description=description.ASSET_ID)
    asset_code: str = Field(description=description.ASSET_CODE)
    tx_id: Optional[str] = Field(description="Transaction id from blockchain")
    amount: Optional[Decimal] = Field(description="Amount of transferred funds")
    commission: Optional[Decimal] = Field(description="Size of blockchain commission")
    transaction_type: str = Field(description="type of transaction", default='withdrawal')
    direction: Optional[str] = Field(description="in/out against system", default='in')
    address_from: Optional[str] = Field(description="source address", default=None)
    address_to: Optional[str] = Field(description="destination address", default=None)

    class Config(CommonConfig):
        collection_name = "transactions"


class FavoritesAssets(base.MongoDbModel):
    user_id: str
    asset_id: str

    class Config(CommonConfig):
        collection_name = "favorite_assets"


class LastPrices(base.MongoDbModel):
    prices: dict
    last_update_time: datetime = datetime.now()

    class Config(CommonConfig):
        collection_name = "last_prices"


class TxFees(base.MongoDbModel):
    data: dict

    class Config(CommonConfig):
        collection_name = "tx_fees"
