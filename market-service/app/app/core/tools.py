import datetime
import random
from calendar import timegm
from collections import defaultdict
from decimal import Decimal
from typing import Any, Optional, Dict

from app.core.config import settings
from api_contrib.core.services import balance_service
from app.core import constants


def get_dealer_deposit(asset_code: str) -> Decimal:
    deposits = balance_service.send_internal('internal/user/deposits', json={
        "user_id": constants.DEALER_USER_ID
    })
    user_balance = Decimal(0)

    for dep in deposits:
        if dep['asset_code'] == asset_code:
            user_balance = dep['amount']
            break

    return user_balance


def query_from_asset_config(filter_key: str, filter_value: str) -> Optional[Dict]:
    for _, asset_config in settings.ASSETS.items():
        for k, v in asset_config.items():
            if k == filter_key and v == filter_value:
                return asset_config
    return None


def get_asset_by_net_code(code: str) -> Optional[Dict]:
    return query_from_asset_config("main_net_code", code)


def dec_to_str(value: Decimal) -> str:
    return f'{value:.8f}'


def to_decimal(value: Any) -> Decimal:
    return Decimal(f'{value:.8f}')


def get_history():
    message = {}
    for i in range(random.randint(1, 5)):
        d = timegm((datetime.datetime.now() - datetime.timedelta(days=i)).timetuple())
        price = random.random()
        message[d] = {
            'ticker': d,
            'price': price,
            'basevolume': (1 + i) * 10,
            'volume': (1 + i) * 10 / price,
            'type': 'BUY' if i % 2 == 0 else 'SELL',
        }

    return message


def get_summary_new(rows):
    result_offers = {
        "buy": defaultdict(dict),
        "sell": defaultdict(dict),
    }

    for order in rows:
        side = order['side'].lower()
        price = Decimal(order['price'])
        amount_base_currency = Decimal(order['volume'])
        amount_quote_currency = order['volume'] * price

        result_offers[side][price]['price'] = price
        result_offers[side][price]['amount_currency'] = amount_base_currency
        result_offers[side][price]['amount_basecurrency'] = amount_quote_currency
        result_offers[side][price]['total_currency'] = amount_base_currency
        result_offers[side][price]['total_basecurrency'] = amount_quote_currency
        result_offers[side][price]['amount_base_currency'] = amount_base_currency
        result_offers[side][price]['amount_quote_currency'] = amount_quote_currency
        result_offers[side][price]['total_base_currency'] = amount_base_currency
        result_offers[side][price]['total_quote_currency'] = amount_quote_currency

    return {
        "buy": dict(result_offers["buy"]),
        "sell": dict(result_offers["sell"])
    }


def get_summary(orders):
    result_offers = defaultdict(dict)
    for order in orders:
        price = Decimal(order['price'])
        asset = Decimal(result_offers[price].get('amount_base_currency', 0))
        amount_base_currency = asset + Decimal(order['quantity'])
        amount_quote_currency = asset * price

        result_offers[price]['price'] = price
        result_offers[price]['amount_currency'] = amount_base_currency
        result_offers[price]['amount_basecurrency'] = amount_quote_currency
        result_offers[price]['total_currency'] = amount_base_currency
        result_offers[price]['total_basecurrency'] = amount_quote_currency

        result_offers[price]['amount_base_currency'] = amount_base_currency
        result_offers[price]['amount_quote_currency'] = amount_quote_currency
        result_offers[price]['total_base_currency'] = amount_base_currency
        result_offers[price]['total_quote_currency'] = amount_quote_currency

    return dict(result_offers)
