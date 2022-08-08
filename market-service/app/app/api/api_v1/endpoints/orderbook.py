from typing import Any, Dict

from api_contrib.core.services import get_current_user
from fastapi import APIRouter, Path, Depends

from app import crud, schemas
from app.core import constants
from app.models import OrderStatus, TradeType

router = APIRouter()


@router.post("/orderbook/", response_model=schemas.OrdersDepthResponse)
async def get_context_orders_all(payload: schemas.MarketFilterById) -> Any:
    """
    Available offers in current market (market level 2 aka "Market depth" implementation)
    """
    market = constants.get_market_by_id(payload.marketid)

    db_document = await crud.order_book.find_one({"symbol": market.symbol})

    return {
        "message": db_document.get('data') if db_document else {}
    }


async def get_orders_from_db(user_id, symbol=None) -> Any:
    query = {
        'user_id': user_id,
        'status': {"$in": [OrderStatus.NEW, OrderStatus.PARTIAL_EXECUTED]}
    }

    if symbol:
        query.update({'symbol': symbol})

    all_orders = await crud.order.find_all(query)

    return schemas.UserOrdersResponse(message={
        TradeType.BUY.lower(): [
            schemas.OrdersLegasy(**order)
            for order in all_orders if order['side'] == TradeType.BUY
        ],
        TradeType.SELL.lower(): [
            schemas.OrdersLegasy(**order)
            for order in all_orders if order['side'] == TradeType.SELL
        ]
    })


@router.post("/my/orderbook/{symbol}/{order_type}/",
             response_model=schemas.UserOrdersResponse,
             response_model_exclude_none=True)
async def get_user_currency_orders(user: Dict = Depends(get_current_user),
                                   symbol: str = Path(...),
                                   order_type: str = Path(...)) -> Any:
    """
    Returns user's opened orders
    """
    return await get_orders_from_db(user['id'], symbol)


@router.post("/my/orderbook/",
             response_model=schemas.UserOrdersResponse,
             response_model_exclude_none=True)
async def get_user_orders(user: Dict = Depends(get_current_user)) -> Any:
    """
    Returns user's opened orders
    """
    return await get_orders_from_db(user['id'])


@router.post("/settled/",
             response_model=schemas.SettledOrderResponse,
             response_model_exclude_none=True)
async def get_user_settled_all(payload: schemas.MarketFilter,
                               user: Dict = Depends(get_current_user)) -> Any:
    """ Return executed trades for user """
    trades = await crud.trade.find_all({
        'symbol': payload.symbol,
        'user_id': user['id']
    }, limit=30)
    return schemas.SettledOrderResponse(message=schemas.SettledOrders(items=[trade for trade in trades]))
