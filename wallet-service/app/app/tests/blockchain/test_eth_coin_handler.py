from datetime import datetime
from unittest.mock import patch

from eth_tester import EthereumTester, MockBackend
from hexbytes import HexBytes
from web3 import EthereumTesterProvider

from app import schemas
from app.blockchain.handlers.ethereum.base import AbstractTransactionFilter
from app.blockchain.handlers.ethereum.eth import EthCoinHandler, EthBlockFilter
from app.core.config import settings
from app.tests.tools import AttrDict


class TestEthBlockFilter:

    def setup(self):
        self.eth_tester = EthereumTester(backend=MockBackend())
        self.handler = EthCoinHandler(asset_code='tETH')
        accounts = self.eth_tester.get_accounts()
        self.transaction_filter = EthBlockFilter(accounts[1], self.handler.web3)
        self.tx_id = self.eth_tester.send_transaction({
            'from': accounts[0],
            'to': accounts[1],
            'gas': 21000,
            'value': 1
        })

    def test_apply_filter(self):
        transaction = self.eth_tester.get_transaction_by_hash(self.tx_id)
        transaction['hash'] = HexBytes(transaction['hash'])
        block_data = AttrDict({"timestamp": int(datetime.now().timestamp())})
        message_data = self.transaction_filter.apply(block_data, AttrDict(transaction))

        assert isinstance(message_data, dict)
        assert 'address' in message_data
        assert 'txid' in message_data
        assert 'value' in message_data
        assert 'status' in message_data
        assert 'date' in message_data


class TestEthCoinHandler:
    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def setup(self, provider):
        self.eth_tester = EthereumTester(backend=MockBackend())
        provider.return_value = EthereumTesterProvider(self.eth_tester)
        self.handler = EthCoinHandler(asset_code='tETH')

    def test__send_to_system_account(self, eth_deposit_address):
        target_address = eth_deposit_address
        value = 1000
        system_account = self.handler._get_system_account()

        balance_before = system_account.balance
        deposit_count_before = system_account.deposit_count

        self.handler._send_to_system_account(target_address, value)

        system_account = self.handler._get_system_account()
        assert system_account.balance > balance_before
        assert system_account.deposit_count == deposit_count_before + 1

    def test_init_deposit_filter(self):
        assert isinstance(EthBlockFilter([], self.handler.web3), AbstractTransactionFilter)

    def test_get_new_address(self):
        address = self.handler.web3.geth.personal.new_account(settings.SECRET_KEY)
        assert isinstance(address, str)
        assert len(address) == 42

    def test_send_withdrawal_transaction(self, mock_user):
        system_account = self.handler._get_system_account()
        balance_before = system_account.balance
        target_address = self.handler.get_new_address()
        tx_id = self.handler.send_withdrawal_transaction(schemas.WithdrawalRequest(
            **{
                'amount': '0.00001',
                'asset_id': settings.ASSETS[self.handler.asset_code]['asset_id'],
                'asset_code': self.handler.asset_code,
                'address': target_address,
                'user_id': mock_user['id']
            }
        ))
        system_account = self.handler._get_system_account()
        assert system_account.balance < balance_before