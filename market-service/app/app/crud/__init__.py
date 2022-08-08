from api_contrib.crud.base_mongo import CRUDBaseMongo

from app.models.market import Market, Favorites, Depth, Executor, OrderBook
from app.models.order import Order as Order
from app.models.trade import Trade
from .market import CRUDMarket
from .order import CRUDOrder
from .trade import CRUDTrade

favorites = CRUDMarket(Favorites)
market = CRUDMarket(Market)

order = CRUDOrder(Order)
trade = CRUDTrade(Trade)
market_depth = CRUDBaseMongo(Depth)
executor = CRUDBaseMongo(Executor)
order_book = CRUDBaseMongo(OrderBook)
