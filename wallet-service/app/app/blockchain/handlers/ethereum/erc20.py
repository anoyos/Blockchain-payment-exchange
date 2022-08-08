from datetime import datetime
from os import getenv
from typing import Any, Optional, Dict

from api_contrib.core.utils import logger

from app import crud, schemas
from app.blockchain.handlers.ethereum.base import EthereumHandler
from app.blockchain.handlers.ethereum.contract import SmartContract, ERC20Contract
from app.blockchain.handlers.ethereum.interface import AbstractTransactionFilter
from app.core.config import settings
from app.schemas.internal import ApplyWithdrawalMessage


class ERC20BlockFilter(AbstractTransactionFilter):

    def __init__(self, token_contract: SmartContract, accounts_to_track: list):
        self.token = token_contract
        self.accounts_to_track = accounts_to_track
        self.precision = self.token.contract.functions.decimals().call()

    def apply(self, block_data: Any, transaction: Any) -> Optional[Dict]:
        if transaction.to == self.token.contract_address:
            try:
                transfer_data = self.token.contract.decode_function_input(transaction.input)[1]

                if transfer_data.get('_to') in self.accounts_to_track and transfer_data['_value'] != 0:
                    db_address = crud.deposit_addresses.find_one_sync({"address": transfer_data['_to'],
                                                                       "asset_code": self.token.asset_code
                                                                       })
                    return {
                        "address": transfer_data['_to'],
                        "user_id": db_address['user_id'],
                        "value": transfer_data['_value'] / 10 ** self.precision,
                        "txid": transaction.hash.hex(),
                        "status": "confirmed",
                        "date": datetime.fromtimestamp(block_data.timestamp)
                    }
            except Exception as e:
                logger.error(e)

        return None


class ERC20Handler(EthereumHandler):

    def __init__(self, asset_code: str, chain_code='ETH') -> None:
        super().__init__(asset_code, chain_code=chain_code)

        # Get coin metadata
        asset = settings.ASSETS.get(asset_code)
        self.token_contract_address = asset['token_contract']
        self.token_decimals = asset['decimal_precision']
        self.token = ERC20Contract(asset_code=self.asset_code,
                                   contract_address=self.token_contract_address,
                                   web3=self.web3,
                                   abi_path=getenv('USDT_ABI_PATH'))

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass

    @property
    def name(self) -> str:
        return 'erc20'

    def _send_to_system_account(self, target_address: str, value: float):
        """
        Transfer `ERC20 tokens` from `deposit` contract to `collector` account
        via call smart contract function
        """
        map_index = self.get_address_storage_index(target_address)
        _ = self.factory_contract.functions.sendFundsFromReceiverTo(
            map_index,
            self.token_contract_address,
            int(value * (10 ** self.token.precision)),
            self.collector_address
        ).transact()

    def _save_system_transaction(self, tx_id):
        # Wait transaction receipt
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_id)

        # Save transaction in history
        _ = crud.transaction.create_sync({
            "user_id": "system",
            "asset_id": settings.ASSETS[self.asset_code]['asset_id'],
            "asset_code": self.asset_code,
            "address": receipt['from'],
            "address_from": receipt['from'],
            "address_to": receipt['to'],
            "amount": 0,
            "commission": (receipt['gasUsed'] * self.web3.eth.gas_price) / 10 ** 18,
            "tx_id": tx_id.hex(),
            "status": "confirmed",
            "transaction_time": datetime.now().isoformat(),
            "transaction_type": "create_contracts",
            "direction": "out"
        })

    def _create_batch_of_contracts(self, batch_size: int):
        tx_id = self.factory_contract.functions.createReceivers(batch_size).transact()
        self._save_system_transaction(tx_id)

    def init_deposit_filter(self) -> AbstractTransactionFilter:
        return ERC20BlockFilter(self.token,
                                accounts_to_track=self.get_address_to_track())

    def send_withdrawal_transaction(self, request: schemas.WithdrawalRequest) -> str:

        amount = int(request.amount) * 10 ** self.token.precision
        from_address = self.web3.eth.default_account
        nonce = self.web3.eth.getTransactionCount(from_address)

        # Build a transaction that invokes this contract's function, called transfer
        token_txn = self.token.contract.functions.transfer(
            request.address,
            amount,
        ).buildTransaction({
            'chainId': 4,
            'gas': 70000,
            'gasPrice': self.web3.eth.gas_price,
            'nonce': nonce,
        })

        signed_txn = self.web3.eth.account.signTransaction(token_txn,
                                                           private_key=self.settings.FACTORY_OWNER_KEY)

        tx_id_hex_bytes = self.web3.eth.sendRawTransaction(signed_txn.rawTransaction)

        tx_id = tx_id_hex_bytes.hex()
        _ = ApplyWithdrawalMessage(tx_id=tx_id,
                                   asset_code=self.asset_code).send(return_result=False)
        return tx_id


class ERC20HandlerRopsten(ERC20Handler):

    def __init__(self, asset_code: str) -> None:
        super().__init__(asset_code, chain_code='ROPSTEN')

    @property
    def name(self) -> str:
        return 'erc20_ropsten'