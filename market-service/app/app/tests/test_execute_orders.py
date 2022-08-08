from unittest.mock import patch

from app.models.order import Order


class CelerySendTaskMock:
    @staticmethod
    def get():
        return {'status': 'success'}


class TestExchangeBroker:

    @patch('app.connections.background.celery_app')
    def test_execute_mock_orders_successfully(self, mock_celery_app, buy_order, sell_order):
        mock_celery_app.send_task.return_value = CelerySendTaskMock
        from app.market.core.broker import MarketBroker
        from app.core import constants
        broker = MarketBroker(market=constants.get_market_by_symbol(buy_order['symbol']))
        order_executed = broker._execute(Order(**buy_order),
                                         Order(**sell_order))
        assert order_executed, True

    @patch('app.connections.background.celery_app')
    def test_execute_real_orders_successfully(self, mock_celery_app):
        from app.market.core.broker import MarketBroker
        from app.core import constants

        mock_celery_app.send_task.return_value = CelerySendTaskMock

        broker = MarketBroker(market=constants.get_market_by_symbol('tBTCtUSDT'))
        broker.process_orders()

        assert True
