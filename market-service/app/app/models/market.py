from datetime import datetime
from decimal import Decimal
from typing import Optional

from api_contrib.models import description
from api_contrib.models.base import MongoDbModel
from pydantic import Field

from .base import CommonConfig


class Favorites(MongoDbModel):
    user_id: str
    market_id: str

    class Config(CommonConfig):
        collection_name = "favorites"


class Market(MongoDbModel):
    currency_id: Optional[str] = Field(description="Deprecated use quote_currency_id field instead")
    market_name: Optional[str] = Field(description="Deprecated use symbol field instead")
    symbol: str
    marketid: Optional[str] = Field(description="Deprecated use `id` or `symbol` field instead")
    base_currency_id: str
    base_currency_code: str
    quote_currency_id: str
    quote_currency_code: str
    last_ticker: Optional[int] = 0
    precision: Optional[int] = Field(description=" Number of decimal places on TradingView Chart", default=2)
    last_price: Optional[Decimal] = 0.0000
    last_change: Optional[Decimal] = 0.0
    price_24: Optional[Decimal] = 0.0000
    high_24: Optional[Decimal] = 0.0000
    low_24: Optional[Decimal] = 0.0000
    change_24: Optional[Decimal] = 0.0000
    volume_24: Optional[Decimal] = 0.0000
    current_bid: Optional[Decimal] = 0.0000
    current_ask: Optional[Decimal] = 0.0000
    last_ticker_run: Optional[int] = 0
    last_real_ticker_run: Optional[int] = 0
    market_visible: Optional[bool] = True
    market_accept_orders: Optional[bool] = True
    featured: Optional[bool] = False
    featured_ranking: Optional[int] = 9999
    is_popular: Optional[bool] = True
    is_hot: Optional[bool] = False
    last_update_time: Optional[datetime] = None

    class Config(CommonConfig):
        collection_name = "markets"


class Executor(MongoDbModel):
    """
    Volume of offer by current price -
    Market level 2 aka "Market depth" implementation)
    """
    uid: str = Field(description="Current replica set which handle broker containers")

    class Config(CommonConfig):
        collection_name = "executor"


class Depth(MongoDbModel):
    """
    Volume of offer by current price -
    Market level 2 aka "Market depth" implementation)
    """
    symbol: str = Field(description="Currency pair, e.g. BTCUSDT")
    side: str = Field(description="Buy or sell")
    price: Decimal = Field(description="Estimate base currency in quote currency")
    volume: Decimal = Field(description="how many coin you can buy/sell on specified price", default=Decimal(0))

    class Config(CommonConfig):
        collection_name = "depth"


class OrderBook(MongoDbModel):
    """
    Volume of offer by current price -
    Market level 2 aka "Market depth" implementation)
    """
    data: str = Field(description="Current summary of orders queue")
    symbol: str = Field(description=description.SYMBOL)

    class Config(CommonConfig):
        collection_name = "orderbook"
