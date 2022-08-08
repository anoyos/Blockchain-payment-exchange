from unittest.mock import patch

from eth_tester import EthereumTester, MockBackend
from web3 import EthereumTesterProvider

from app.tests.conftest import USER


class TestDepositUSDT:
    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def setup(self, provider):
        from app.blockchain.handlers.ethereum.erc20 import ERC20Handler

        eth_tester = EthereumTester(backend=MockBackend())
        provider.return_value = EthereumTesterProvider(eth_tester)
        self.handler = ERC20Handler(asset_code='tUSDT')
        # self.tran_address = self.handler.get_new_address()
        self.test_tx_id = 'test_tx_id'
        self.asset_code = self.handler.asset_code
        self.mock_user = USER
        self.deposit_request = {}
        # super().clear_deposit_data()

    @patch('app.schemas.internal.celery_app')
    def test_deposit_process(self, celery_app):
        """
            Process full deposit flow.
            Require geth node and address with real balance in Rinkby network
         """
        # from app.blockchain.handlers.ethereum.erc20 import ERC20Handler
        # handler = ERC20Handler(asset_code='tUSDT'

        self.handler.run_new_block_scan()




