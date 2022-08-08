import itertools
from typing import Optional, List, Dict, Tuple, Set

import requests
from api_contrib.core.utils import logger
from pydantic import BaseModel

from app import crud
from app import schemas
from app.core.config import settings
from app.models import Market

USDT_ASSET_NAME = 'USDT'


def get_liquid_markets_symbols() -> Optional[Set[str]]:
    markets_endpoint = f'{settings.B2BX_URL}/frontoffice/api/info'

    try:
        response = requests.get(url=markets_endpoint)
        response.raise_for_status()
    except Exception as e:
        logger.error(e, exc_info=True)
        return

    # format of symbol: eth_usdt
    return set(k for k in response.json()['pairs'].keys())


class _Asset(BaseModel):
    asset_id: str
    short_name: str
    is_quote_asset: bool
    main_net_code: str


def make_asset_pairs() -> List[Tuple[_Asset, _Asset]]:
    assets: Dict[str, _Asset] = {k: _Asset(**v) for k, v in settings.ASSETS.items()}
    base_assets = [a for a in assets.values() if not a.is_quote_asset]
    quote_assets = [a for a in assets.values() if a.is_quote_asset]
    usd_asset = [a for a in quote_assets if a.main_net_code == USDT_ASSET_NAME].pop()

    # Create pairs by product `base` and `quotes` coins
    # [('XLT', 'BTC'), ('XLT', 'USDT'), ('DASH', 'BTC'), ('DASH', 'USDT')]
    base_quote_pairs: List[Tuple[_Asset, _Asset]] = list(itertools.product(base_assets, quote_assets))

    # Create pair of by product `quotes` between itself quoted by `MAIN` coin
    # [('BTC', 'USDT'), ('ETH', 'USDT')]
    quote_assets.remove(usd_asset)
    quote_quote_pairs: List[Tuple[_Asset, _Asset]] = list(itertools.product(quote_assets, [usd_asset]))

    return [*base_quote_pairs, *quote_quote_pairs]


class _MarketCreate(schemas.MarketCreate):
    main_net_symbol: str


def make_market(base: _Asset, quote: _Asset) -> _MarketCreate:
    symbol = f'{base.short_name}{quote.short_name}'
    # format: eth_usdt
    main_net_symbol = f'{base.main_net_code.lower()}_{quote.main_net_code.lower()}'

    return _MarketCreate(
        base_currency_id=base.asset_id,
        base_currency_code=base.short_name,
        quote_currency_id=quote.asset_id,
        quote_currency_code=quote.short_name,
        symbol=symbol,
        main_net_symbol=main_net_symbol
    )


def actualize_markets():
    current_markets: List[Market] = crud.market.find_obj_sync()
    current_symbols = set(m.symbol for m in current_markets)

    markets_from_config = [make_market(*asset_pair) for asset_pair in make_asset_pairs()]
    actual_main_net_symbols = get_liquid_markets_symbols()
    actual_markets = \
        [
            schemas.MarketCreate(**m.dict())
            for m in markets_from_config if m.main_net_symbol in actual_main_net_symbols
        ] if actual_main_net_symbols else markets_from_config
    actual_symbols = set(m.symbol for m in actual_markets)

    to_delete = [m for m in current_markets if m.symbol not in actual_symbols]
    for m in to_delete:
        crud.market.delete_one_sync({'symbol': m.symbol})
        logger.info(f'Market {m.symbol} was deleted')

    to_create = [m for m in actual_markets if m.symbol not in current_symbols]
    for m in to_create:
        crud.market.insert_one_sync(m)
        logger.info(f'Market {m.symbol} was created')


def init_db() -> None:
    """actual_symbols
    Fill database collections with coins and trading pairs from config file
    """
    # Actualize `markets` collection in database
    actualize_markets()


if __name__ == '__main__':
    init_db()
