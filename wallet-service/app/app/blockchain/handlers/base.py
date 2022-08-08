from abc import abstractmethod
from typing import Any, Dict, Optional

from api_contrib.core.utils import logger

from app import crud, schemas
from app.core.constants import AddressStatus
from app.core.tools import get_asset_id_by_code


class CoinHandler:

    def __init__(self, asset_code: str):
        super().__init__()
        self.asset_code = asset_code

    def __enter__(self):
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @abstractmethod
    def calc_fee(self, amount: str) -> str:
        pass

    @abstractmethod
    def estimate_fee(self) -> str:
        pass

    @abstractmethod
    def get_new_address(self) -> str:
        pass

    @abstractmethod
    def _finalize_deposit(self, deposit_request: Any, transaction: Any) -> None:
        pass

    @abstractmethod
    def send_withdrawal_transaction(self, request: schemas.WithdrawalRequest) -> str:
        pass

    def _process_in_transaction(self, transaction: Optional[Dict]) -> None:
        if not transaction:
            return

        logger.info(f'start {self.asset_code} deposit for {transaction["address"]}')

        # Read transaction data
        tran_address = transaction['address']
        tx_id = transaction['txid']

        # Find uncompleted deposit request for address from transaction input:
        deposit_request = crud.deposit_addresses.find_one_sync({
            'address': tran_address,
            'status': AddressStatus.UNUSED,
            'asset_code': self.asset_code
        })
        # Find transaction in database  by id
        db_transaction = crud.transaction.find_one_sync({
            'address': tran_address,
            'tx_id': tx_id
        })

        # If deposit request exists and transaction not processed earlier
        if deposit_request and not db_transaction:
            message_data = {
                "user_id": deposit_request["user_id"],
                "asset_id": get_asset_id_by_code(self.asset_code),
                "asset_code": self.asset_code,
                "address": tran_address,
                "amount": transaction["value"],
                "tx_id": tx_id,
                "status": transaction["status"],
                "transaction_time": transaction["date"].isoformat(),
                "transaction_type": "deposit",
                "direction": "in"
            }

            # if result.status == ResponseStatus.SUCCESS:
            # Finalize request depending on scenario for particular coin
            self._finalize_deposit(deposit_request, transaction)

            # Save transaction in history
            _ = crud.transaction.create_sync(message_data)

            # Send message to balance service
            message = schemas.ApplyTransactionMessage(**message_data)
            result = message.send()
            logger.info(f"Deposit process status: {result.status}")

    def get_address_for_user(self, user_id: str) -> str:
        """ Create new address for user deposit operation and save link with address and user_id """
        # TODO: share this code across the coins
        # Get address from pool, if user already requested it.
        address_record = crud.deposit_addresses.find_one_sync({
            'status': AddressStatus.UNUSED,
            'user_id': user_id,
            'asset_code': self.asset_code
        })
        # if user already requests address for deposit - use it
        if address_record:
            return address_record['address']
        else:
            deposit_address = self.get_new_address()

            # save user deposit request address
            crud.deposit_addresses.save_address_for_user({
                'user_id': user_id,
                'address': deposit_address,
                'currency_name': self.asset_code,
                'asset_code': self.asset_code,
                'asset_id': get_asset_id_by_code(self.asset_code)
            })

            # Add address to scan-procedure filter
            return deposit_address
