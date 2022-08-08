from unittest.mock import patch

import pytest
from api_contrib.core.services import get_current_user
from api_contrib.schemas.base import ResponseStatus
from eth_tester import EthereumTester, MockBackend
from fastapi.testclient import TestClient
from web3 import EthereumTesterProvider

from app.core.config import settings
from app.tests.conftest import USER, USER_2


def get_user():
    return USER


def get_user2():
    return USER_2


class TestDepositAddress:
    @pytest.mark.parametrize("asset", settings.ASSETS)
    @pytest.mark.parametrize("user_id", [0, 1])
    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def test_get_deposit_address(self, provider, user_id, asset, client: TestClient):
        provider.return_value = EthereumTesterProvider(EthereumTester(backend=MockBackend()))
        if user_id == 0:
            client.app.dependency_overrides[get_current_user] = get_user
        else:
            client.app.dependency_overrides[get_current_user] = get_user2

        response = client.post(
            f"{settings.API_V1_STR}/depositaddress/", json={
                "currencyid": settings.ASSETS[asset]['asset_id']
            }
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS
