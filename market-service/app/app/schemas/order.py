from decimal import Decimal
from typing import Optional, Dict, List, Any, Union

from api_contrib.schemas.base import ResponseFormat
from pydantic import BaseModel, Field

from app.models.order import Order
from app.models.market import Depth


class CreateOrderRequest(Order):
    user_id: Optional[str]


class CancelOrderRequest(BaseModel):
    order_id: str


class OrdersDepth(BaseModel):
    price: str = Field(description="Price of offer")
    amount_currency: Optional[str] = Field(description="Deprecated. Use `amount_quote_currency` field instead")
    amount_basecurrency: Optional[str] = Field(description="Deprecated. Use `amount_base_currency` field instead")
    total_currency: Optional[str] = Field(description="Deprecated. Use `total_quote_currency` field instead")
    total_basecurrency: Optional[str] = Field(description="Deprecated. Use `total_base_currency` field instead")
    amount_quote_currency: str = Field(description="Total value of quote currency offer")
    amount_base_currency: str = Field(description="Total value of base currency offer")
    total_quote_currency: str = Field(description="Total cost of all offers in quote currency units")
    total_base_currency: str = Field(description="Total cost of all offers in base currency units")


class OrdersDepthResponse(ResponseFormat):
    message: Dict[str, Any]


class OrdersLegasy(Order):
    orderid: Optional[str] = Field(description="Deprecated field use `id` field instead")
    marketid: Optional[str] = Field(description="Deprecated field use `symbol` field instead")
    amount_currency: Optional[Decimal] = Field(description="Deprecated field")
    amount_basecurrency: Optional[Decimal] = Field(description="Deprecated field use `quantity` field instead")
    datestamp: Optional[int] = Field(description="Deprecated field use `create_date` field instead")
    user_basecurrency_fee: Optional[Decimal] = Field(description="Deprecated field. Commission "
                                                                 "will taken when order will ne executed")
    user_currency_fee: Optional[Decimal] = Field(description="Deprecated field. Commission "
                                                             "will taken when order will ne executed")

    def __init__(self, **data):
        super().__init__(**data)


class UserOrdersResponse(ResponseFormat):
    message: Dict[str, List[OrdersLegasy]]


class CreateOrderResponse(ResponseFormat):
    message: OrdersLegasy
