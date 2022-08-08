import datetime
from decimal import Decimal
from unittest.mock import patch

from app import crud
from app.blockchain.handlers.bitcoinlib.base import BitcoinlibHandler
from app.core import tools
from app.core.constants import AddressStatus


class TestDepositBTC:

    def setup(self):
        self.address = 'nVWHeF1d3pgZwRbpTsz7qNdFLoHoTw4zLe'
        self.tx_id = '94d1d485eb3203a95c601b572ad1a4aa1f93c2c27a0e0b785bf36de7443ad4c5'
        self.mock_transactions = [{
            'spending_txid': None,
            'value': tools.satoshi_to_btc(Decimal(10000000000)),
            'address': self.address,
            'script': b'v\xa9\x14\x0ee\xc5\xcaa`)\xdf_\xba\xd1\r\xc2\x86\xd1\x08\xb7QG\xd5\x88\xac',
            'output_n': 0,
            'spending_index_n': None,
            'spent': False,
            'script_type': 'p2pkh',
            'key_id': 27,
            'transaction_id': 1,
            'transaction': [],
            'block_height': 3202599,
            'date': datetime.datetime(2021, 6, 8, 12, 17, 16),
            'confirmations': 7921,
            'txid': self.tx_id,
            'network_name': 'dogecoin_testnet',
            'status': 'confirmed',
            'is_output': False
        }]
        # clear data from from prev test
        request = crud.deposit_addresses.find_one_sync({"address": self.address})
        crud.deposit_addresses.update_sync(request, {
            'status': AddressStatus.UNUSED
        })
        crud.transaction.delete_one_sync({"tx_id": self.tx_id})

    @patch('app.schemas.internal.celery_app')
    @patch('app.blockchain.handlers.bitcoinlib.base.Wallet')
    @patch('app.blockchain.handlers.bitcoinlib.base.get_new_session')
    def test_deposit(self, session, wallet, celery_app):
        celery_app.send_task.return_value.get.return_value = {"id": 'celery_mock_task_id', 'status': 'success'}
        with BitcoinlibHandler(asset_code='tBTC') as handler:
            for transaction in self.mock_transactions:
                handler._process_in_transaction(transaction)
