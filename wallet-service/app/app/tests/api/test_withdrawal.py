from unittest.mock import patch

import pytest
from api_contrib.schemas.base import ResponseStatus
from eth_tester import EthereumTester, MockBackend
from fastapi.testclient import TestClient
from web3 import EthereumTesterProvider

from app.core.config import settings
from app.core.constants import SERVICE_BTC_ADDRESS


class TestFees:
    def test_tx_fees_for_all_coin(self, client: TestClient):
        response = client.post(
            f"{settings.API_V1_STR}/withdraw/get_coin_tx_fees/", json={
            }
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS


class TestWithdrawalRoute:

    @pytest.mark.parametrize("asset_code", ["tETH", "tBTC"])
    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def test_get_commission(self, provider, asset_code, client: TestClient):
        provider.return_value = EthereumTesterProvider(EthereumTester(backend=MockBackend()))
        response = client.post(
            f"{settings.API_V1_STR}/withdraw/get_commission/", json={
                "asset_id": settings.ASSETS[asset_code]['asset_id'],
                "amount": '0.00019001',
                "address": SERVICE_BTC_ADDRESS
            }
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS

    @pytest.mark.parametrize("asset_code", ["tETH", "tBTC"])
    @patch('app.schemas.internal.celery_app')
    @patch('app.api.api_v1.endpoints.withdrawal.blockchain_handlers')
    def test_withdrawal_confirm(self,
                                blockchain_handlers,
                                celery_app,
                                asset_code,
                                client: TestClient) -> None:
        blockchain_handlers.get.return_value.__enter__.return_value \
            .send_withdrawal_transaction.return_value = 'test_tx_id'

        celery_app.send_task.return_value.get.return_value = {"id": 'celery_mock_task_id', 'status': 'ok'}
        response = client.post(
            f"{settings.API_V1_STR}/withdraw/", json={
                "asset_id": settings.ASSETS[asset_code]['asset_id'],
                "asset_code": asset_code,
                "amount": "0.00019001",
                "commission": "0.00001024",
                "address": SERVICE_BTC_ADDRESS
            }
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS
