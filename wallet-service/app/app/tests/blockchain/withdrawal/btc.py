from unittest.mock import patch

from app import schemas
from app.blockchain.handlers.factory import blockchain_handlers
from app.core.config import settings
from app.core.constants import SERVICE_BTC_ADDRESS


class TestBtcOutTransaction:
    @patch('app.blockchain.handlers.bitcoinlib.base.Wallet')
    @patch('app.blockchain.handlers.bitcoinlib.base.get_new_session')
    def test_send(self, session, wallet, mock_user):
        """
        test sending blockchain transaction
        :param mock_user:
        :return:
        """
        asset_code = 'tBTC'
        fake_tx_id = 'fake_tx_id'
        wallet.return_value.send_to.return_value.txid = fake_tx_id
        with blockchain_handlers.get(asset_code) as handler:
            tx_id = handler.send_withdrawal_transaction(
                schemas.WithdrawalRequest(
                    **{
                        'amount': '0.00001024',
                        'commission': '0.00001024',
                        'asset_id': settings.ASSETS[asset_code]['asset_id'],
                        'asset_code': asset_code,
                        'address': SERVICE_BTC_ADDRESS,
                        'user_id': mock_user['id']
                    }
                )
            )
            assert tx_id == fake_tx_id
