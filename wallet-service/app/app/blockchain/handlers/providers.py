from web3 import Web3


def get_eth_provider(url: str = None) -> Web3.HTTPProvider:
    """ Provides  opportunity to mock ethereum node connection in unit tests """
    return Web3.HTTPProvider(url)
