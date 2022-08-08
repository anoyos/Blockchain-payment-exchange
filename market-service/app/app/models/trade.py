from datetime import datetime
from decimal import Decimal

from api_contrib.models import base, description
from pydantic import Field
from typing import Optional

from .base import CommonConfig


class TradeType:
    BUY = "BUY"
    SELL = "SELL"


class Trade(base.MongoDbModel):
    create_date: datetime = Field(default_factory=datetime.utcnow, description="Record creation time")
    user_id: str = Field(description=description.USER_ID)
    side: str = Field(description="BUY/SELL type of operation")
    symbol: str = Field(description=description.SYMBOL)
    price: str = Field(description="Price of trade operation in quote currency units (ex in BTC)")
    quantity: str = Field(description="Quantity of base currency")
    value: Decimal = Field(description="Price x Quantity = total cost of trade in quote currency (ex in BTC) ")
    commission: Decimal = Field(description="System commission in in quote currency (ex in BTC)")
    base_currency_id: str = Field(description=description.BASE_CURRENCY_ID)
    base_currency_code: str = Field(description=description.BASE_CURRENCY_CODE)
    quote_currency_id: str = Field(description=description.QUOTE_CURRENCY_ID)
    quote_currency_code: str = Field(description=description.QUOTE_CURRENCY_CODE)
    order_id: Optional[str] = Field(description="Order identifier this trade was created from")

    class Config(CommonConfig):
        collection_name = "trades"
