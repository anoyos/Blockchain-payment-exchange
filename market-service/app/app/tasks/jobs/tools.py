from decimal import Decimal
from typing import List

import requests

from app import crud
from app import models
from app.core.config import settings
from app.core.tools import get_asset_by_net_code, get_dealer_deposit


def _define_size_for_auto_trade(market: models.Market,
                                current_price: float,
                                all_markets: List[models.Market]) -> Decimal:
    """
    Pair BTC/USDT

    I want to BUY/SELL X quantity of BTC.
    But I want to save sufficient funds into USDT (quote currency) account.
    So X, should be following:

    X = volume_in_usd / current_price_in_usd

    where volume_in_usd:

    volume_in_usd = quote_currency_balance * ( 1 / number_of_pairs_quoted_in_usd ) * LIQUIDITY_RESERVE_CONSTANT

    """
    quote_currency = market.quote_currency_code
    quote_currency_balance = get_dealer_deposit(quote_currency)
    # quote_currency_balance = 600
    number_of_pairs = len([m for m in all_markets
                           if m.quote_currency_code == quote_currency])

    volume_in_usd = Decimal(quote_currency_balance) * Decimal(1 / number_of_pairs) * settings.LIQUIDITY_RESERVE_CONSTANT

    size_for_trade = volume_in_usd / Decimal(current_price)

    return size_for_trade


def get_prices(quote_currency: str, price_only=True) -> dict:
    vs_currency = 'USD' if quote_currency == 'USDT' else quote_currency
    price_endpoint = f'{settings.STAT_API_URL}?vs_currency={vs_currency}' \
                     f'&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    result = {}
    response = requests.get(price_endpoint)
    response.raise_for_status()
    data = response.json()

    quote_asset = get_asset_by_net_code(quote_currency)

    for item in data:

        base_asset = get_asset_by_net_code(item['symbol'].upper())

        if not base_asset:
            continue

        market = crud.market.find_one_sync({
            "base_currency_code": base_asset["short_name"],
            "quote_currency_code": quote_asset["short_name"]
        })

        if market:
            result[market["symbol"]] = f"{item['current_price']:.8f}" if price_only else item

    return result
