from app import crud
from app.market.core.events import generate_market_stat
from app.models import Order


class TestEvents:

    def test_generate_market_stat(self, buy_order):
        order = Order(**buy_order)
        market_state = crud.market.find_one_sync({"symbol": order.symbol})
        message = generate_market_stat(order, market_state)
        assert message
