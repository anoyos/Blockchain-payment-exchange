from datetime import datetime
from decimal import Decimal
from typing import Optional

from api_contrib.models.base import MongoDbModel
from pydantic import Field

from .base import CommonConfig


class OrderType:
    """
    Stock orders type
    https://www.investopedia.com/investing/basics-trading-stock-know-your-orders/
    """
    LIMIT = "LIMIT"
    MARKET = "MARKET"


class OrderStatus:
    NEW = "NEW"
    PARTIAL_EXECUTED = "PARTIAL_EXECUTED"
    EXECUTED = "EXECUTED"
    CANCELED = "CANCELED"


class TimeInForce:
    """
    https://www.investopedia.com/terms/t/timeinforce.asp
    """
    GTC = "GTC"  # Good Till Cancel
    FOK = "FOK"  # Fill or Kill


class Order(MongoDbModel):
    create_date: datetime = Field(default_factory=datetime.utcnow, description="Time, when order was created")
    user_id: Optional[str]
    symbol: str
    side: str
    type: str = Field(default=OrderType.LIMIT, description="Stock orders type")
    quantity: Decimal
    price: Decimal
    time_in_force: str = Field(default=TimeInForce.GTC, description="Long an order will remain active")
    status: Optional[str] = Field(default=OrderStatus.NEW, description="Execution status")

    class Config(CommonConfig):
        collection_name = "orders"
