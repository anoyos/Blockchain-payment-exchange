import json
from typing import Any

from web3 import Web3
from web3.middleware import geth_poa_middleware


class SmartContract:

    def __init__(self,
                 asset_code: str,
                 contract_address: str,
                 abi_path: str,
                 web3: Any = None,
                 rpc_url: str = 'http://localhost:8545',
                 ) -> None:

        self.asset_code = asset_code
        self.contract_address = contract_address
        self.abi_path = abi_path

        if web3:
            self.web3 = web3
        else:
            self.web3 = Web3(Web3.HTTPProvider(rpc_url))
            # handle blocks output correctly
            self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    def __enter__(self):
        return self.contract

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @staticmethod
    def _load_abi_from_file(abi_path):
        with open(abi_path) as fp:
            data = json.load(fp)
        return data['abi'] if 'abi' in data else data['result']

    @property
    def contract(self):
        return self.web3.eth.contract(self.web3.toChecksumAddress(self.contract_address),
                                      abi=self._load_abi_from_file(self.abi_path))


class ERC20Contract(SmartContract):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.precision = self.contract.functions.decimals().call()
