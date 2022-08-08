from typing import Dict

from api_contrib.core.services import get_current_user
from api_contrib.schemas.base import ResponseStatus
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.exceptions import HTTPException

from app import crud
from app import schemas
from app.core import constants, config
from app.market.core.broker import MarketBroker
from app.tasks.worker import balance

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/login/"
)

router = APIRouter()


@router.post("/order/")
async def create_order(*,
                       user: Dict = Depends(get_current_user),
                       payload: schemas.CreateOrderRequest) -> schemas.CreateOrderResponse:
    """ Create order on the platform """
    # Add user auth data
    payload.user_id = user['id']

    # Try lock balance for settled order
    locked_status = balance.lock_balance_for_order(order=payload)
    if locked_status.status == ResponseStatus.ERROR:
        raise HTTPException(status_code=400, detail=locked_status.message)

    # Place order into Market depth
    market_broker = MarketBroker(market=constants.get_market_by_symbol(payload.symbol))
    market_broker.create_order(payload)
    del market_broker

    return schemas.CreateOrderResponse(message=schemas.OrdersLegasy(**payload.dict()))


@router.post("/cancelorder/", response_model=schemas.TextResponse)
async def cancel_order(payload: schemas.CancelOrderRequest,
                       user: Dict = Depends(get_current_user)) -> schemas.TextResponse:
    """  Cancel the specified order """
    order = await crud.order.find_one({'id': payload.order_id}, return_obj=True)

    if order.user_id != user['id']:
        return schemas.TextResponse(message='OPERATION DO NOT PERMITTED', status='error')

    market_broker = MarketBroker(market=constants.get_market_by_symbol(order.symbol))
    market_broker.cancel_order(order)
    del market_broker
    return schemas.TextResponse(message='SUCC_ORDER_CLOSED')
