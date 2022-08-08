from decimal import Decimal
from unittest.mock import patch

from app.core import constants
from app.tasks.jobs.robot import _define_size_for_auto_trade
from app.tasks.jobs.robot import create_orders


class TestOrderRobot:

    @patch('app.tasks.jobs.robot._define_size_for_auto_trade')
    def test_create_order_by_script(self, mock_trade_size):
        mock_trade_size.return_value = 1
        create_orders()

    @patch('app.tasks.jobs.tools.get_dealer_deposit')
    def test_get_size_for_auto_trade(self, dealer_deposits):
        dealer_deposits.return_value = Decimal(100)
        market = constants.ALL_MARKETS[0]
        quantity = _define_size_for_auto_trade(market, 100, constants.ALL_MARKETS)
        assert isinstance(quantity, Decimal)
