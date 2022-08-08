from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Dict

from app import schemas
from app.blockchain.handlers.ethereum.base import AbstractTransactionFilter
from app.blockchain.handlers.ethereum.base import EthereumHandler
from app.schemas.internal import ApplyWithdrawalMessage


class EthBlockFilter(AbstractTransactionFilter):

    def __init__(self, accounts_to_track, web3):
        self.all_accounts = accounts_to_track
        self.web3 = web3

    def apply(self, block_data: Any, transaction: Any) -> Optional[Dict]:
        if transaction.to in self.all_accounts and transaction.value != 0:
            receipt = self.web3.eth.get_transaction_receipt(transaction.hash)
            if receipt.status == 1:

                status = "successful"
                value = self.web3.fromWei(transaction.value, 'ether')
            else:
                status = "revert"
                value = Decimal(0)
            return {
                "address": transaction.to,
                "value": value,
                "txid": transaction.hash.hex(),
                "status": status,
                "date": datetime.fromtimestamp(block_data.timestamp)
            }
        else:
            return None


class EthCoinHandler(EthereumHandler):

    def __init__(self, asset_code: str, chain_code: str = 'ETH') -> None:
        super().__init__(asset_code, chain_code)

    def _send_to_system_account(self, target_address: str, value: float):
        """
        Transfer Ether from `deposit` contract to `collector` account
        via call smart contract function
        """
        if value > 0:
            map_index = self.get_address_storage_index(target_address)
            _ = self.factory_contract.functions.sendETHTo(
                int(map_index),
                self.web3.toWei(value, 'ether'),
                self.collector_address
            ).transact()

    def init_deposit_filter(self) -> AbstractTransactionFilter:
        accounts_to_track = self.get_address_to_track()
        return EthBlockFilter(accounts_to_track, self.web3)

    def send_withdrawal_transaction(self, request: schemas.WithdrawalRequest) -> str:
        gas = 21000
        amount_in_wei = self.web3.toWei(float(request.amount), 'ether')
        val = amount_in_wei - (gas * self.web3.eth.gas_price)
        tx_id_hex_bytes = self.web3.eth.send_transaction({
            'to': request.address,
            'value': val,
            'gas': gas
        })
        tx_id = tx_id_hex_bytes.hex()
        _ = ApplyWithdrawalMessage(tx_id=tx_id,
                                   asset_code=self.asset_code).send(return_result=False)

        return tx_id


class BNBCoinHandler(EthCoinHandler):

    def __init__(self, asset_code: str) -> None:
        super().__init__(asset_code, chain_code='BSC')
