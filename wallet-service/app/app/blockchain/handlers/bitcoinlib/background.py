import logging

from api_contrib.core.utils import logger
from bitcoinlib.wallets import WalletError

from app.blockchain.handlers.bitcoinlib.base import BitcoinlibHandler
from app.core.config import settings

logger.setLevel(logging.INFO)


def send_new_transaction_to_ledger():
    """
    Scan blockchain for new transaction and send outputs to ledger
    """
    for asset_code in settings.ASSETS:
        try:
            bitcoinlib_handler = BitcoinlibHandler(asset_code)
            with bitcoinlib_handler as handler:
                handler.process_deposit()
        except WalletError:
            logger.info(f"skip {asset_code}")
