from api_contrib.core.services import auth_service

from app import crud
from app.models.market import Market
from app.models.trade import TradeType

db_markets = crud.market.find_all_sync()

MARKET_IDS = dict([(m['id'], m) for m in db_markets])
ALL_MARKETS = crud.market.find_obj_sync()
MARKETS_BY_SYMBOL = dict([(m['symbol'], m) for m in db_markets])


def get_mock_market() -> dict:
    for m in db_markets:
        if m['market_name'] == 'XLT-tBTC':
            return m
    return {
        "symbol": "no_data_found"
    }


MOCK_MARKET = get_mock_market()


def get_market_by_symbol(symbol: str) -> Market:
    return Market(**MARKETS_BY_SYMBOL.get(symbol))


def get_market_by_id(market_id: str) -> Market:
    return Market(**MARKET_IDS.get(market_id))


def get_market_id_by_symbol(symbol: str) -> str:
    return get_market_by_symbol(symbol).id


def get_symbol_by_market(market_id: str) -> str:
    return MARKET_IDS[market_id]['symbol']


MOCK_BUY_ORDER = {
    "id": "608be2bc79e658cb2638cedf",
    "user_id": "6059ca50b695b1142c11c7bf",
    "symbol": MOCK_MARKET['symbol'],
    "side": TradeType.BUY,
    "quantity": "1",
    "price": "2.00002",
    "time_in_force": "FOK"
}

MOCK_SELL_ORDER = {
    "id": "608be2bc79e658cb2638cede",
    "user_id": "6059ca50b695b1142c11c7bm",
    "symbol": MOCK_MARKET['symbol'],
    "side": TradeType.SELL,
    "quantity": "1",
    "price": "4.0000",
    "time_in_force": "FOK"
}


def get_dealer_user() -> str:
    user = auth_service.send_internal('internal/get_dealer')
    return user['id']


DEALER_USER_ID = get_dealer_user()
