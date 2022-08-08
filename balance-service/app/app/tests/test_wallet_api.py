import pytest
from fastapi.testclient import TestClient

from app.core.config import settings


class TestWalletEndpoints:
    @pytest.mark.parametrize("endpoint", [
        'wallet/ledger',
        'wallet/ledgerexport/list'
    ])
    def test_wallet_endpoints_base(self, endpoint, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/{endpoint}/", json={},
        )
        content = response.json()
        assert content["status"] == 'success'
