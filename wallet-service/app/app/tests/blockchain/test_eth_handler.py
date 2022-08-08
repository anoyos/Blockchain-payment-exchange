from decimal import Decimal
from unittest.mock import patch

from eth_tester import EthereumTester, MockBackend
from web3 import EthereumTesterProvider

from app.blockchain.handlers.ethereum.base import EthereumHandler


class TestEthereumHandler:
    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def setup(self, provider):
        provider.return_value = EthereumTesterProvider(EthereumTester(backend=MockBackend()))
        self.handler = EthereumHandler(asset_code='tETH')

    def test_get_network_latest(self):
        assert isinstance(self.handler._get_network_latest(), int)

    def test_get_latest_read_block(self):
        result = self.handler._get_latest_read_block()
        assert isinstance(result, dict)
        assert len(result) > 0

    def test_get_system_account(self):
        from app.models.blockchain import SystemAccount
        result = self.handler._get_system_account()
        assert isinstance(result, SystemAccount)
        assert result.asset_code == self.handler.asset_code

    def test_update_system_account_by_deposit(self):
        system_account = self.handler._get_system_account()
        balance_before = system_account.balance
        deposit_count_before = system_account.deposit_count
        value = 1000
        self.handler._update_system_account_by_deposit(system_account, value)
        system_account = self.handler._get_system_account()

        assert system_account.balance == balance_before + value
        assert system_account.deposit_count == deposit_count_before + 1

    def test_calc_fee(self):
        fee = self.handler.calc_fee(Decimal(1000))
        assert Decimal(fee) != Decimal(0)
        assert isinstance(fee, str)

    def test_run_new_block_scan(self):

        net_block_before = self.handler._get_network_latest()
        last_read_block_before = self.handler._get_latest_read_block()['last_read_block_num']

        self.handler.run_new_block_scan()

        last_read_block = self.handler._get_latest_read_block()['last_read_block_num']

        if net_block_before > last_read_block_before:
            assert last_read_block > last_read_block_before
        else:
            assert last_read_block <= last_read_block_before


