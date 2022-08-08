import datetime
from unittest.mock import patch

from eth_tester import EthereumTester, MockBackend
from web3 import EthereumTesterProvider

from app.blockchain.handlers.ethereum.eth import EthCoinHandler
from app.tests import conftest
from app.tests import tools


class TestDepositETH:
    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def setup(self, provider):
        eth_tester = EthereumTester(backend=MockBackend())
        provider.return_value = EthereumTesterProvider(eth_tester)
        self.handler = EthCoinHandler(asset_code='tETH')
        self.tran_address = self.handler.get_new_address()
        self.test_tx_id = 'test_tx_id'
        self.asset_code = self.handler.asset_code
        self.mock_user = conftest.USER
        self.deposit_request = {}
        tools.clear_deposit_data(self)

    @patch('app.schemas.internal.celery_app')
    def test_deposit_process(self, celery_app):
        """
            Process full deposit flow.
            Require geth node and address with real balance in Rinkby network
        """
        self.handler._process_in_transaction({
            "address": self.tran_address,
            "txid": self.test_tx_id,
            "value": 0.001,
            "status": "confirmed",
            "date": datetime.datetime.now()
        })
