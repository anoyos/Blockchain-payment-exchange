from unittest.mock import patch

import pytest
from api_contrib.schemas.base import ResponseStatus

from app import schemas
from app.core.constants import MOCK_BUY_ORDER, MOCK_SELL_ORDER
from app.tasks.jobs.tools import get_prices


class TestTasks:

    @pytest.mark.parametrize("order", [MOCK_BUY_ORDER, MOCK_SELL_ORDER])
    @patch('app.tasks.worker.balance.celery_app')
    def test_lock_balance(self, celery_app, order) -> None:
        from app.tasks.worker.balance import lock_balance_for_order

        celery_app.send_task.return_value.get.return_value = {
            "id": 'celery_mock_task_id',
            'status': ResponseStatus.SUCCESS
        }

        lock_status = lock_balance_for_order(schemas.CreateOrderRequest(**order))
        assert lock_status.status == ResponseStatus.SUCCESS


class TestTaskTools:

    def test_get_asset_by_net_code(self):
        prices = get_prices('USDT')
        assert isinstance(prices, dict)
