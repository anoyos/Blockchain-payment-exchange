from typing import Optional, Dict, List
from uuid import UUID

from api_contrib.schemas.base import ResponseFormat, BaseModel

from app.models.market import Market


class MarketSchema(Market):
    pass


class MarketFilter(BaseModel):
    symbol: Optional[str]


class MarketFilterById(BaseModel):
    marketid: str


class MarketArrayResponse(ResponseFormat):
    message: Dict[str, MarketSchema]


class MarketCreate(Market):
    pass


class MarketUpdate(Market):
    currency_id: Optional[UUID]
    base_currency_id: Optional[UUID]
    market_name: Optional[str]


class MarketResponse(ResponseFormat):
    message: Dict[UUID, Market]


class FavoritesResponse(ResponseFormat):
    message: List[str]


class FavoritesAction:
    ADD = 'add'
    REMOVE = 'remove'

