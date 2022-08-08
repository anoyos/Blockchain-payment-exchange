from typing import Dict
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.core.constants import MOCK_BUY_ORDER, MOCK_SELL_ORDER
from api_contrib.schemas.base import ResponseStatus


class TestAPIResponse:
    @pytest.mark.parametrize("endpoint", [
        '/all/'
    ])
    def test_endpoints_no_payload(self, endpoint, client: TestClient) -> None:
        response = client.post(f"{settings.API_V1_STR}{endpoint}")
        assert response.json().get('message')

    @pytest.mark.parametrize("endpoint", [
        '/ticker/',
        '/trades/',
    ])
    def test_endpoints_market_id_payload(self, endpoint, client: TestClient, market_filter_id: Dict) -> None:
        response = client.post(f"{settings.API_V1_STR}{endpoint}", json=market_filter_id)
        assert response.json().get('message')

    @pytest.mark.parametrize("filter_by_symbol", [True, False])
    def test_get_user_orders(self, filter_by_symbol, market_filter, client: TestClient) -> None:
        symbol = market_filter['symbol']
        endpoint = f'/my/orderbook/{symbol}/both/' if filter_by_symbol else '/my/orderbook/'
        response = client.post(f"{settings.API_V1_STR}{endpoint}")
        content = response.json()
        assert content["status"] == "success"
        assert isinstance(content["message"]["buy"], list)
        assert isinstance(content["message"]["sell"], list)

    def test_get_market_depth(self, market_filter_id, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/orderbook/", json=market_filter_id,
        )
        content = response.json()
        assert content["status"] == "success"
        assert isinstance(content["message"]["buy"], list)
        assert isinstance(content["message"]["sell"], list)

    @pytest.mark.parametrize("order", [MOCK_BUY_ORDER, MOCK_SELL_ORDER])
    @patch('app.api.api_v1.endpoints.orders.balance')
    def test_create_order(self, balance_worker, order, client: TestClient) -> None:

        balance_worker.lock_balance_for_order.status.return_value = ResponseStatus.SUCCESS

        response = client.post(
            f"{settings.API_V1_STR}/order/",
            headers={"Authorization": "Bearer my_test_token"},
            json=order,
        )
        content = response.json()
        assert content["status"] == 'success'

    @pytest.mark.parametrize("filter_by_symbol", [True, False])
    def test_get_trades(self, filter_by_symbol, market_filter, client: TestClient) -> None:
        payload = market_filter if filter_by_symbol else {}
        response = client.post(
            f"{settings.API_V1_STR}/settled/", json=payload,
        )
        content = response.json()
        assert content["status"] == "success"
        assert len(content["message"]) > 0
