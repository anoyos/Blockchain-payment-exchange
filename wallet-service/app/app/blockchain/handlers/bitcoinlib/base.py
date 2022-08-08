from decimal import Decimal

from api_contrib.core.utils import logger
from bitcoinlib.db import get_new_session
from bitcoinlib.values import Value
from bitcoinlib.wallets import Wallet

from app import crud, schemas
from app.blockchain.handlers.base import CoinHandler
from app.core import tools
from app.core.constants import AddressStatus, KeyScanStatus
from app.core.constants import SERVICE_BTC_ADDRESS


class BitcoinlibHandler(CoinHandler):

    def __init__(self, asset_code: str):
        super().__init__(asset_code)

        self.db_session = get_new_session()
        self.wallet = Wallet(asset_code, session=self.db_session)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is None:
            self.db_session.commit()

        self.db_session.close()

    @property
    def name(self) -> str:
        return 'btclib'

    def get_new_address(self) -> str:
        """ generate new address to transfer founds into main wallet."""
        new_key = self.wallet.new_key()
        deposit_address = new_key.address
        new_key.set_scan_status(KeyScanStatus.NEW)
        return deposit_address

    def estimate_fee(self):
        db_row = crud.transaction.find_min(self.asset_code)
        return self.calc_fee(amount=str(db_row['min_value']),
                             address=db_row['_id'])

    def calc_fee(self, amount: str, address: str = SERVICE_BTC_ADDRESS) -> Decimal:
        """ Calculate blockchain commission for output transaction """
        try:
            transaction_value = f'{amount} {self.asset_code.upper()}'
            est_fee = self.wallet.transaction_create(output_arr=[(address, transaction_value)],
                                                     return_fee=True)

            fee = Value.from_satoshi(int(est_fee), network=self.wallet.network).str_unit(currency_repr='symbol')
        except Exception as e:
            logger.error(e, exc_info=True)
            return Decimal(0)
        return fee.split(' ')[0]

    def _finalize_deposit(self, request, transaction):
        # Set deposit request as used in Project Database
        crud.deposit_addresses.update_sync(request, {
            'status': AddressStatus.USED
        })

        # Remove address from transaction search list in Blockchain Database.
        self.wallet.key(transaction["address"]).set_scan_status(KeyScanStatus.SCANNED)

    def process_deposit(self):
        logger.info(f"start scan {self.asset_code} wallet")
        self.wallet.scan(scan_status=KeyScanStatus.NEW)
        self.db_session.commit()

        for transaction in self.wallet.transactions(as_dict=True):
            if not transaction['is_output']:
                transaction['value'] = tools.satoshi_to_btc(Decimal(transaction["value"]))
                self._process_in_transaction(transaction)

    def send_withdrawal_transaction(self, request: schemas.WithdrawalRequest) -> str:
        """ Sent transaction to blockchain """

        transaction = self.wallet.send_to(request.address,
                                          f'{request.amount} {self.asset_code}',
                                          fee=tools.btc_to_satoshi(request.commission))

        return transaction.txid