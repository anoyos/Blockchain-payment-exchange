from abc import abstractmethod
from decimal import Decimal

from api_contrib.core.utils import logger
from eth_account import Account
from web3 import Web3
from web3.middleware import construct_sign_and_send_raw_middleware
from web3.middleware import geth_poa_middleware

from app import schemas, crud
from app.blockchain.handlers.base import CoinHandler
from app.blockchain.handlers.ethereum.contract import SmartContract
from app.blockchain.handlers.ethereum.interface import AbstractTransactionFilter, DummyTransactionFilter
from app.blockchain.handlers.providers import get_eth_provider
from app.core import tools
from app.core.config import ChainSetting


class EthereumHandler(CoinHandler):

    def __init__(self, asset_code: str, chain_code='ETH') -> None:
        super().__init__(asset_code)
        self.asset_code = asset_code
        self.pool_interval = 2
        self.settings = ChainSetting(chain_code=chain_code)

        # Create web3 instance and middleware
        self.web3 = self._init_web3()

        # Create contract from environment
        self.factory_contract = SmartContract(asset_code=self.asset_code,
                                              contract_address=self.settings.FACTORY_CONTRACT_ADDRESS,
                                              abi_path=self.settings.FACTORY_CONTRACT_ABI_PATH,
                                              web3=self.web3,
                                              ).contract
        # Read settings value from environment
        self.collector_address = self.web3.eth.default_account
        self.batch_size = self.settings.RECEIVERS_BATCH_SIZE

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def _init_web3(self):
        web3 = Web3(get_eth_provider(self.settings.RPC_URL))
        # handle blocks output correctly
        web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # auto sign transactions with token contract
        acct = Account.from_key(self.settings.FACTORY_OWNER_KEY)
        web3.middleware_onion.add(construct_sign_and_send_raw_middleware(acct))
        web3.eth.default_account = acct.address

        return web3

    @abstractmethod
    def _send_to_system_account(self, target_address, value: float):
        pass

    def _get_network_latest(self) -> int:
        block = self.web3.eth.get_block('latest')
        return block.number

    def _get_system_account(self):
        return crud.system_account.find_one_sync({
            'asset_code': self.asset_code
        }, return_obj=True)

    def _get_latest_read_block(self) -> dict:
        """ Get last block number read by system"""
        return crud.blocks.get_or_create({'asset_code': self.asset_code})

    def get_address_storage_index(self, target_address: str) -> int:
        db_row = crud.deposit_addresses.find_one_sync({
            "address": target_address,
            "asset_code": self.asset_code
        })
        return int(db_row['mapping_num'])

    @staticmethod
    def _update_system_account_by_deposit(system_account, value):
        crud.system_account.update_obj_sync(system_account, {
            "balance": system_account.balance + value,
            "deposit_count": system_account.deposit_count + 1
        })

    def _finalize_deposit(self, request, transaction):
        logger.info(f"{self.asset_code}: finalize {transaction}")
        self._send_to_system_account(transaction['address'], transaction['value'])

    def get_address_to_track(self):
        data = crud.deposit_addresses.find_all_sync(query={"user_id": {"$ne": None},
                                                           "asset_code": self.asset_code})
        return [row['address'] for row in data]

    def get_new_address(self):
        """
        Get address from pool have already generated by `generate_deposit_addresses` merhod
        """
        return crud.deposit_addresses.get_free_address(self.asset_code)

    @abstractmethod
    def send_withdrawal_transaction(self, request: schemas.WithdrawalRequest) -> str:
        pass

    def init_deposit_filter(self) -> AbstractTransactionFilter:
        return DummyTransactionFilter()

    def estimate_fee(self):
        return self.calc_fee(Decimal('0'))

    def calc_fee(self, amount: Decimal) -> str:
        return str(self.web3.fromWei(21000 * self.web3.eth.gas_price, 'ether'))

    def run_new_block_scan(self):
        net_block = self._get_network_latest()
        last_read_block = self._get_latest_read_block()
        block_num = last_read_block['last_read_block_num'] if last_read_block['last_read_block_num'] > 0 \
            else net_block - 1

        deposit_filter = self.init_deposit_filter()

        logger.info(
            f"{self.asset_code}: last_read_block: {block_num}, last_net_block: "
            f"{net_block}, scan next {net_block - block_num} blocks")
        while block_num < net_block:
            block_num += 1
            data = self.web3.eth.get_block(block_num, full_transactions=True)
            for transaction in data.transactions:
                transaction_data = deposit_filter.apply(block_data=data,
                                                        transaction=transaction)
                self._process_in_transaction(transaction_data)

            crud.blocks.update_sync(last_read_block, {"last_read_block_num": block_num})

    def _get_last_db_mapping_index(self) -> int:
        last_db_contract = crud.deposit_addresses.find_all_sync(query={'asset_code': self.asset_code},
                                                                limit=1,
                                                                order_by=[('mapping_num', -1)])
        map_item_num = 0 if not last_db_contract else last_db_contract[0]['mapping_num']
        return map_item_num

    def _save_new_contracts(self):

        map_item_num = self._get_last_db_mapping_index()
        while True:
            map_item_num += 1
            address = self.factory_contract.functions.receiversMap(map_item_num).call()

            if address == '0x0000000000000000000000000000000000000000':
                break

            crud.deposit_addresses.create_sync({
                "address": address,
                "asset_code": self.asset_code,
                "asset_id": tools.get_asset_id_by_code(self.asset_code),
                "currency_name": self.asset_code,
                "mapping_num": map_item_num
            })

    def generate_deposit_addresses(self):
        # how many contracts already created
        free_addresses = crud.user_contracts.find_all_sync(query={"user_id": None,
                                                                  "asset_code": self.asset_code})

        if len(free_addresses) < self.batch_size:
            # Create N contracts in blockchain
            # TODO: fix error in contract call
            # self._create_batch_of_contracts(self.batch_size)

            # Read and save N elements from mapping
            self._save_new_contracts()
