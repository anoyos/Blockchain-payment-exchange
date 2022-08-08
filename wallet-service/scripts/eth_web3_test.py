from app import crud
from app.blockchain.handlers.ethereum.base import EthereumHandler
from app.core.config import settings

USDT_TOKEN_CONTRACT_RINKEBY = '0xD92E713d051C37EbB2561803a3b5FBAbc4962431'

import json
import time

from web3 import Web3


class EthereumObserver:

    def __init__(self, contract_address, infura_project_id):
        infura_project_id = 'ffe4471302f14290825ab5e828a017fa'
        contract_address = '0x7D88d79E8819859689a3134EB31e8F88eC6d5B73'
        self.web3 = Web3(Web3.HTTPProvider(f'https://kovan.infura.io/v3/{infura_project_id}'))

        compiled_path = f'/Users/davydov/projects/proxify/nordanwind/brownie_contracts/bullflag/build/deployments/42/{contract_address}.json'
        with open(compiled_path) as fp:
            self.abi = json.load(fp)['abi']

        self.contract = self.web3.eth.contract(address=contract_address,
                                               abi=self.abi)

        self.block_filter = self.web3.eth.filter({'fromBlock': 'latest', 'address': contract_address})

    def handle_event(self, event):
        receipt = self.web3.eth.waitForTransactionReceipt(event['transactionHash'])
        result = self.contract.events.MyEvent.processReceipt(receipt)
        print(result[0]['args'])

    def run_event_listener(self):
        while True:
            for event in self.block_filter.get_new_entries():
                print(event)
                self.handle_event(event)
                time.sleep(2)

    def test():
        observer = EthereumObserver(infura_project_id='ffe4471302f14290825ab5e828a017fa',
                                    contract_address='0x7D88d79E8819859689a3134EB31e8F88eC6d5B73')

        observer.run_event_listener()



class CLIHandler(EthereumHandler):

    @staticmethod
    def get_abi():
        abi_path = '/Users/davydov/projects/proxify/nordanwind/brownie_contracts/bullflag/build/contracts/Factory.json'
        with open(abi_path) as fp:
            data = json.load(fp)
        return data['abi']

    def get_contact(self, contract_address: str = USDT_TOKEN_CONTRACT_RINKEBY):
        contract_checksum = self.web3.toChecksumAddress(contract_address)
        abi = self.get_usdt_abi() if contract_address == USDT_TOKEN_CONTRACT_RINKEBY else self.get_abi()
        contract = self.web3.eth.contract(contract_checksum, abi=abi)

        return contract

    @staticmethod
    def get_usdt_abi():
        project_root = '/Users/davydov/projects/proxify/nordanwind/wallet-service'
        with open(f'{project_root}/app/app/blockchain/handlers/ethereum/usdt_abi.json') as fp:
            abi = json.load(fp)
        return abi

    def get_balance_of_token(self, address):
        contract = self.get_contact()
        validated_address = self.web3.toChecksumAddress(address)
        amount = contract.functions.balanceOf(validated_address).call()
        return amount

    def gp(self):
        return self.web3.eth.gas_price

    def token_transfer(self,
                       from_address=None,
                       to_address=None,
                       amount=None):
        system_account = crud.system_account.find_one_sync({
            'asset_code': self.asset_code
        }, return_obj=True)

        self.web3.geth.personal.unlock_account(system_account.address, settings.SECRET_KEY)
        self.web3.geth.personal.unlock_account(from_address, settings.SECRET_KEY)

        contract = self.get_contact()

        resp = self.web3.eth.send_transaction({
            'from': system_account.address,
            'to': USDT_TOKEN_CONTRACT_RINKEBY,
            'data': contract.functions.transfer(to_address, amount).transact({'from': from_address}),
            'value': 0,
            'gasPrice': self.web3.eth.gas_price,
            'gas': 100000
        })
        print(resp)

        self.web3.geth.personal.lock_account(system_account.address)

    def token_transfer1(self,
                        from_address=None,
                        to_address=None,
                        amount=None):
        contract = self.get_contact()
        self.web3.geth.personal.unlock_account(from_address, settings.SECRET_KEY)
        tx_hash = contract.functions.transfer(to_address, amount).transact({'from': from_address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt)

    def test_erc20_interface(self):
        contract = self.get_contact()
        data = contract.functions.name().call()
        print(data)

    def deposit_flow(self):
        """
        In Accordance with
        https://ethereum.stackexchange.com/questions/64686/collecting-erc20-balances-from-multiple-addresses

        1) Create N (e.g. 100) contracts by scheduler
        2) Read mapping
        System Account (for TUSDT): 0xF9997CB792634ff814173889371F723E4729e983


        """
        pass

    def load_private_key(self):
        key_path = '/Users/davydov/.geth-rinkeby/keystore/UTC--2021-07-01T11-43-51.128205400Z--f9997cb792634ff814173889371f723e4729e983'
        with open(key_path) as keyfile:
            encrypted_key = keyfile.read()
            private_key = self.web3.eth.account.decrypt(encrypted_key, settings.SECRET_KEY)

        print(private_key.hex())

    def send_funds_from_receiver(self):
        sys_address = '0xF9997CB792634ff814173889371F723E4729e983'
        contract = self.get_contact('0xCc225E5A6ad35DC52136f3ACb91C038f9f7cfCEb')
        self.web3.geth.personal.unlock_account(sys_address, settings.SECRET_KEY)
        resp = contract.functions.sendFundsFromReceiverTo(1,
                                                          USDT_TOKEN_CONTRACT_RINKEBY,
                                                          2000000,
                                                          sys_address).transact(
            {'from': sys_address})
        print(resp)

    def create_receivers(self):
        contract = self.get_contact('0xCc225E5A6ad35DC52136f3ACb91C038f9f7cfCEb')
        sys_address = '0xF9997CB792634ff814173889371F723E4729e983'
        self.web3.geth.personal.unlock_account(sys_address, settings.SECRET_KEY)
        tx_id = contract.functions.createReceivers(8).transact(
            {'from': sys_address})

        self.web3.geth.personal.lock_account(sys_address)
        return tx_id.hex()

    def get_receiver(self):
        contract = self.get_contact('0xCc225E5A6ad35DC52136f3ACb91C038f9f7cfCEb')
        return contract.functions.receiversMap(111).call()

    @staticmethod
    def test_case():
        pass


def load_abi_from_file(abi_path):
    with open(abi_path) as fp:
        data = json.load(fp)
    return data['abi'] if 'abi' in data else data['result']


def _parse_block(h, block_num: int, address: str):
    data = h.web3.eth.get_block(block_num, full_transactions=True)

    for transaction in data.transactions:

        if transaction.to == address:
            receipt = h.web3.eth.get_transaction_receipt(transaction.hash)

def parse_block():
    from app.blockchain.handlers.ethereum.eth import EthCoinHandler

    h = EthCoinHandler(asset_code='tBNB', chain_code='BSC')
    _parse_block(h, 15045796, '0x6503c0Af1Ddf078eF4D0938431586E1DAF9cF2B5')


if __name__ == '__main__':
    parse_block()