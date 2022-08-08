from app.schemas.balance import LockBalancePayload, CeleryMessage

from app.connections.background import celery_app
from app.schemas.order import CreateOrderRequest
from api_contrib.core.constants import TradeType
from app.core.constants import get_market_by_symbol


def lock_balance_for_order(order: CreateOrderRequest):

    market = get_market_by_symbol(order.symbol)

    if order.side == TradeType.BUY:
        asset_id_for_lock = market.quote_currency_id
        size_for_lock = order.price * order.quantity
    else:
        asset_id_for_lock = market.base_currency_id
        size_for_lock = order.quantity

    locked_msg = CeleryMessage(model=LockBalancePayload(user_id=order.user_id,
                                                        asset_id=asset_id_for_lock,
                                                        amount=size_for_lock),
                               celery_app=celery_app)

    return locked_msg.send()
