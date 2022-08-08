from api_contrib.core.utils import logger

from app import crud
from app.blockchain.handlers.ethereum.base import EthereumHandler
from app.blockchain.handlers.factory import blockchain_handlers


def send_new_transaction_to_ledger():
    """
    Scan blockchain for new transaction and send outputs to ledger
    """
    for asset_code, handler_class in blockchain_handlers.handlers.items():
        if issubclass(handler_class, EthereumHandler):
            logger.info(f"scan blocks for {asset_code}")
            handler = blockchain_handlers.get(asset_code=asset_code)
            with handler:
                try:
                    handler.run_new_block_scan()
                except Exception as e:
                    logger.error(e, exc_info=True)
                    logger.error(f"Scan {asset_code} blockchain failed")


def new_contracts_for_deposit():
    for asset_code, handler_class in blockchain_handlers.handlers.items():
        if issubclass(handler_class, EthereumHandler):
            handler = blockchain_handlers.get(asset_code)
            handler.generate_deposit_addresses()


def process_withdrawal_transaction(message: dict):
    asset_code = message['asset_code']
    tx_id = message['tx_id']
    handler = EthereumHandler(asset_code=asset_code)

    _ = handler.web3.eth.wait_for_transaction_receipt(tx_id)

    system_account = crud.system_account.find_one_sync({"asset_code": asset_code},
                                                       return_obj=True)

    crud.system_account.update_after_withdrawal(obj=system_account,
                                                balance=handler.web3.eth.get_balance(system_account.address))
