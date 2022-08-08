from decimal import Decimal
from typing import Optional, List, Dict

from api_contrib.schemas.base import ResponseFormat
from pydantic import BaseModel, Field

from app.models.trade import Trade


class TradeLegacy(Trade):
    ticker: Optional[int] = Field(description="Deprecated field use `create_date` instead")
    time: Optional[str] = Field(description="Deprecated field, use `create_date` instead")
    basevolume: Optional[str] = Field(description="Deprecated field")
    volume: Optional[str] = Field(description="Deprecated field, use `quantity` instead")
    type: Optional[str] = Field(description="Deprecated field, use `side` instead")

    def __init__(self, **data):
        super().__init__(**data)
        # copy model values into deprecated fields for back compatibility
        self.ticker = int(self.create_date.timestamp())
        self.time = self.ticker
        self.basevolume = f"{Decimal(self.quantity) * Decimal(self.price):.8f}"
        self.volume = self.quantity
        self.type = self.side


class Settled(Trade):
    settleid: Optional[str] = Field(description="Deprecated field")
    tradetype: Optional[str] = Field(description="Deprecated field")
    orderid: Optional[str] = Field(description="Deprecated field")
    currencyid: Optional[str] = Field(description="Deprecated field")
    basecurrencyid: Optional[str] = Field(description="Deprecated field")
    amount_currency: Optional[str] = Field(description="Deprecated field")
    amount_basecurrency: Optional[str] = Field(description="Deprecated field")
    fee_basecurrency: Optional[Decimal] = Field(description="Deprecated field")
    datestamp: Optional[int] = Field(description="Deprecated field")
    notice_read: Optional[int] = Field(description="Deprecated field")

    def __init__(self, **data):
        super().__init__(**data)
        # copy model values into deprecated fields for back compatibility
        # self.settleid = self.id
        # self.orderid = self.id
        # self.tradetype = self.side
        # self.currencyid = self.quote_currency_id
        # self.basecurrencyid = self.base_currency_id
        # self.amount_currency = self.quantity
        # self.amount_basecurrency = f"{Decimal(self.quantity) * Decimal(self.price):.8f}"
        # self.fee_basecurrency = self.commission
        # self.datestamp = int(self.create_date.timestamp())
        # self.notice_read = 0


class Pagination(BaseModel):
    items: int = Field(description="How many items in current page", default=1)
    pages: int = Field(description="How many pages total in page", default=1)
    page: int = Field(description="Number of current page", default=1)
    perpage: int = Field(description="How many items in each page", default=1)


class SettledOrders(BaseModel):
    pagination: Pagination = Pagination()
    items: List[Settled]


class SettledOrderResponse(ResponseFormat):
    message: SettledOrders


class TradeHistoryResponse(ResponseFormat):
    message: Dict[str, TradeLegacy]
