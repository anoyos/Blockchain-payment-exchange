from decimal import Decimal
from typing import Dict

from api_contrib.core.http import ClientHttp
from api_contrib.core.services import get_current_user
from api_contrib.core.utils import logger
from fastapi import APIRouter, Depends

from app import crud
from app import schemas
from app.core import contants, tools
from app.core.config import settings

router = APIRouter()


@router.post("/total_in_usd/", response_model=schemas.BalanceInUSDTResponse)
async def get_usd_balances(user: Dict = Depends(get_current_user)):
    """
    Return user balances quoted in usdt
    """

    market_service = ClientHttp(url=settings.MARKET_SERVICE_URL)
    all_pairs = market_service.send('all')
    last_prices = dict([
        (m['base_currency_code'], m['last_price'])
        for m_id, m in all_pairs.items()
        if m['quote_currency_code'] == settings.TOTAL_BALANCE_CURRENCY
    ])
    user_balances = await crud.balance.find_all({
        'user_id': user['id']
    })
    total_in_usd = 0
    for bal in user_balances:
        price_in_usd = 1 if bal['asset_code'] == settings.TOTAL_BALANCE_CURRENCY else \
                                Decimal(last_prices.get(bal['asset_code'], 0))
        coin_balance = bal['balance']

        if coin_balance != 0 and price_in_usd:
            total_in_usd += coin_balance * price_in_usd

    return {
        "message": {
            "total_in_usd": round(total_in_usd, 2)
        }
    }


@router.post("/balances/", response_model=schemas.BalanceResponse)
async def get_balances(user: Dict = Depends(get_current_user)):
    """
    Return user balances in all currencies
    """
    try:
        asset_code = contants.BASE_ASSET['short_name']
        user_balances = await crud.balance.get_or_create_user_balances({
            'user_id': user['id'],
            'asset_id': contants.BASE_ASSET['asset_id'],
            'asset_code': asset_code
        })

        balances = {}
        for balance in user_balances:
            balance['settings'] = tools.merge_settings(balance['asset_code'], balance.get('settings'))
            balances[balance['asset_id']] = schemas.BalanceLegacy(**balance)

        return schemas.BalanceResponse(message=balances)
    except Exception as e:
        logger.error(e, exc_info=True)
        return schemas.BalanceResponse(message={"error": str(e)},
                                       status=schemas.ResponseStatus.ERROR)