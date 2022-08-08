from fastapi import APIRouter

from app import crud
from app import schemas
from app.core.constants import get_symbol_by_market
router = APIRouter()


async def get_trades(market_id: str) -> schemas.TradeHistoryResponse:
    symbol = get_symbol_by_market(market_id)
    trades = await crud.trade.find_all({'symbol': symbol}, limit=10)

    format_trades = dict([(trade['id'], schemas.TradeLegacy(**trade)) for trade in trades])
    return schemas.TradeHistoryResponse(message=format_trades)


@router.post("/ticker/", response_model=schemas.TradeHistoryResponse)
async def get_tickers(payload: schemas.MarketFilterById) -> schemas.TradeHistoryResponse:
    """ Return market trades old url"""
    return await get_trades(payload.marketid)


@router.post("/trades/", response_model=schemas.TradeHistoryResponse)
async def get_tickers_new_url(payload: schemas.MarketFilterById) -> schemas.TradeHistoryResponse:
    """ Return market trades new url """
    return await get_trades(payload.marketid)
