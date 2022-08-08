from unittest.mock import patch
from datetime import datetime
import pytest
from eth_tester import EthereumTester, MockBackend
from hexbytes import HexBytes
from web3 import EthereumTesterProvider
from web3 import Web3

from app import schemas
from app.blockchain.handlers.ethereum.base import EthereumHandler
from app.blockchain.handlers.ethereum.erc20 import SmartContract, ERC20BlockFilter, ERC20Handler
from app.blockchain.handlers.ethereum.interface import AbstractTransactionFilter
from app.core.config import settings
from app.tests.tools import AttrDict

ASSET_CODE = 'tUSDT'


@pytest.fixture(scope="module")
def eth_tester():
    eth_tester = EthereumTester(backend=MockBackend())
    return eth_tester


@pytest.fixture(scope="module")
def accounts(eth_tester):
    return eth_tester.get_accounts()


@pytest.fixture(scope="module")
def tx_id(eth_tester, accounts):
    return eth_tester.send_transaction({
        'from': accounts[0],
        'to': accounts[1],
        'gas': 21000,
        'value': 1
    })


class TestERC20Contract:

    def test_test_create_instance(self):
        assert SmartContract('contract_address', 'abi_path')

    def test__load_abi_from_file(self):
        pass

    def test_contract(self):
        pass


class TestERC20BlockFilter:

    def test_apply_filter(self):
        asset = settings.ASSETS.get(ASSET_CODE)
        transaction_filter = ERC20BlockFilter(accounts_to_track=['0x736a679E692296CE9aa478b1Fd5079D803f9337A'],
                                              asset_code='tUSDT',
                                              token_contract=asset['token_contract'])
        mock_transaction = AttrDict({
            'blockHash': HexBytes('0xf16a76de243952fd579dede3189f67f2a07ebc156c9dde8ba29f01650b31f14a'),
            'blockNumber': 9002651,
            'from': '0x8325898A207cB7DF7579AA3c214D17412d29a9E6',
            'gas': 34536,
            'gasPrice': 1000000000,
            'hash': HexBytes('0x17a738011718b4c58628e78b823689bc2423e7590ede49d8d80c521a9b7f1346'),
            'input': '0xa9059cbb000000000000000000000000736a679e692296ce9aa478b1fd5079d803f9337a00000000000000000000000000000000000000000000000000000000000f4240',
            'nonce': 22, 'r': HexBytes('0x52802540073f8ee3246ef413644f9ef2d9055724920472ee69d5c740227fa4a1'),
            's': HexBytes('0x74c67a20db4596dc796e2f9cd1a455d1f12bede54984ca23b1e0277022ee239c'),
            'to': '0xD92E713d051C37EbB2561803a3b5FBAbc4962431',
            'transactionIndex': 11,
            'type': '0x0',
            'v': 44,
            'value': 0
        })
        message_data = transaction_filter.apply(block_data=AttrDict({"timestamp": int(datetime.now().timestamp())}),
                                                transaction=mock_transaction)

        assert isinstance(message_data, dict)
        assert 'address' in message_data
        assert 'txid' in message_data
        assert 'value' in message_data
        assert 'status' in message_data
        assert 'date' in message_data


class TestERC20Handler:

    @patch('app.blockchain.handlers.ethereum.base.get_eth_provider')
    def setup(self, provider):
        self.eth_tester = EthereumTester(backend=MockBackend())
        provider.return_value = EthereumTesterProvider(self.eth_tester)
        self.handler = ERC20Handler(asset_code=ASSET_CODE)

    def test___init__(self):
        result = ERC20Handler(asset_code=ASSET_CODE)
        assert isinstance(result, EthereumHandler)

    def test__init_web3(self):
        result = self.handler._init_web3()
        assert isinstance(result, Web3)

    # def test__send_to_system_account(self):
    #     target_address = crud.deposit_addresses.find_one_sync({
    #         "asset_code": self.handler.asset_code
    #     })['address']
    #
    #     result = self.handler._send_to_system_account(target_address, 1.0)
    #     assert result

    def test__save_system_transaction(self, tx_id):
        def get_mock_receipt(*args):
            """
            How to get sample data:
            1) Find real smart-contract transaction here
            https://rinkeby.etherscan.io/tx/0x538c170ff0b3057199b6c481cf2bffcd8106e82527b9a78b11337823341fb330

            2) Get Receipt via web3 call:
            >> from web3 import Web3
            >> w3 = Web3(Web3.HTTPProvider('https://rinkeby.infura.io/v3/ffe4471302f14290825ab5e828a017fa'))
            >> receipt = w3.eth.get_transaction_receipt(
            >>     '0x538c170ff0b3057199b6c481cf2bffcd8106e82527b9a78b11337823341fb330')
            >> print(dict(receipt))
            """
            return {
                'blockHash': HexBytes('0x75636713ed1c16847f654611f126db6df011b9559899838e53294b7564c3a2d4'),
                'blockNumber': 9043881,
                'contractAddress': None,
                'cumulativeGasUsed': 10257480,
                'effectiveGasPrice': '0x3b9aca0a',
                'from': '0xF9997CB792634ff814173889371F723E4729e983',
                'gasUsed': 195738,
                'logs': [],
                'logsBloom': HexBytes('0x0'),
                'status': 1,
                'to': '0xCc225E5A6ad35DC52136f3ACb91C038f9f7cfCEb',
                'transactionHash': HexBytes(tx_id),
                'transactionIndex': 13,
                'type': '0x0'
            }

        patcher = patch('web3.eth.wait_for_transaction_receipt',
                        new=get_mock_receipt)
        patcher.start()

        result = self.handler._save_system_transaction(HexBytes(tx_id))
        patcher.stop()

        assert result is None

    # def test__create_batch_of_contracts(self):
    #     result = self.handler._create_batch_of_contracts(1)
    #     assert result is None

    def test__get_last_db_mapping_index(self):
        result = self.handler._get_last_db_mapping_index()
        assert isinstance(result, int)

    def test__save_new_contracts(self):
        result = self.handler._save_new_contracts()
        assert result is None

    def test_get_address_to_track(self):
        result = self.handler.get_address_to_track()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_init_deposit_filter(self):
        result = self.handler.init_deposit_filter()
        assert isinstance(result, AbstractTransactionFilter)

    def test_generate_deposit_addresses(self):
        result = self.handler.generate_deposit_addresses()
        assert result is None

    def test_get_new_address(self):
        result = self.handler.get_new_address()
        assert isinstance(result, str)

    def test_send_withdrawal_transaction(self, mock_user):
        target_address = self.handler.get_new_address()
        result = self.handler.send_withdrawal_transaction(schemas.WithdrawalRequest(
            **{
                'amount': '0.00001',
                'asset_id': settings.ASSETS[self.handler.asset_code]['asset_id'],
                'asset_code': self.handler.asset_code,
                'address': target_address,
                'user_id': mock_user['id']
            }
        ))
        assert result == 'not_implemented_yet'
