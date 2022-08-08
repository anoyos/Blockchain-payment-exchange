from decimal import Decimal
from os import getenv
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


class TestEndpoints:
    @pytest.mark.parametrize("endpoint", [
        'deposits',
        'withdrawals'
    ])
    def test_common_endpoints(self, endpoint, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/{endpoint}/", headers={
                "Authorization": f"Bearer {getenv('CLUSTER_API_KEY')}"
            }, json={
                "user_id": "test"
            }
        )
        content = response.json()
        assert content["status"] == 'success'

    def test_collections_api(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/internal/user/deposits/", headers={
                "Authorization": f"Bearer {getenv('CLUSTER_API_KEY')}"
            }, json={
                "user_id": "test"
            }
        )
        content = response.json()
        assert isinstance(content, list)

    @patch('app.core.tools.wallet_service')
    def test_balances_api(self, mock_wallet_service, client: TestClient) -> None:
        mock_wallet_service.send.return_value.__getitem__.return_value = Decimal(0.001)
        response = client.post(
            f"{settings.API_V1_STR}/balances/", headers={
                "Authorization": f"Bearer {getenv('CLUSTER_API_KEY')}"
            }, json={
                "user_id": "test"
            }
        )
        content = response.json()
        assert content["status"] == 'success'

    def test_summary_report(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/summary_report/", headers={
                "Authorization": f"Bearer {getenv('CLUSTER_API_KEY')}"
            }, json={
                "asset_code": "tBTC"
            }
        )
        content = response.json()
        assert content["status"] == 'success'
