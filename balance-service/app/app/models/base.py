from datetime import datetime
from decimal import Decimal

from api_contrib.models import description, base
from pydantic import Field
from typing import Optional
from app.core.config import settings
from app.db.engine import client_sync, client


class CommonConfig:
    database_name = settings.MONGODB_NAME
    db_client = client
    db_client_sync = client_sync


class Transaction(base.MongoDbModel):
    user_id: str = Field(description=description.USER_ID)
    asset_id: str = Field(description=description.ASSET_ID)
    asset_code: str = Field(description=description.ASSET_CODE)
    amount: Decimal = Field(description="Size of operation in BTC units")
    address: str = Field(description="Destination address of operation")
    tx_id: str = Field(description="Blockchain transaction unique identifier")
    transaction_time: Optional[datetime] = Field(description="Time when transaction executed in blockchain")
    applied_time: Optional[datetime] = Field(description="Time when operation was applied to user balance")

