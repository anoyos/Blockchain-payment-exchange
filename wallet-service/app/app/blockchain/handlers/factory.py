from typing import Type, Union

from app.core.config import settings
from .base import CoinHandler
from .bitcoinlib.base import BitcoinlibHandler
from .ethereum.base import EthereumHandler
from .ethereum.erc20 import ERC20Handler, ERC20HandlerRopsten
from .ethereum.eth import EthCoinHandler, BNBCoinHandler

HandlerType = Type[CoinHandler]
HandlerClass = Union[BitcoinlibHandler, EthereumHandler]


class HandlersFactory:
    def __init__(self):
        self.handlers = {}
        self.handler_classes = {}

    def register(self, asset_code: str, handler_class: HandlerType):
        self.handlers[asset_code] = handler_class

    def register_class(self, handler_class: HandlerType):
        self.handler_classes[handler_class.__name__] = handler_class

    def map_coins_to_handlers(self):

        for coin, config in settings.ASSETS.items():
            handler_class = self.handler_classes.get(config.get('handler', ''))
            if handler_class:
                self.handlers[coin] = handler_class

    def get(self, asset_code: str) -> HandlerClass:
        try:
            return self.handlers[asset_code](asset_code)
        except KeyError:
            raise NotImplemented(f"Blockchain handler for {asset_code} not found")


blockchain_handlers = HandlersFactory()

# Register handlers for coins
blockchain_handlers.register_class(BitcoinlibHandler)
blockchain_handlers.register_class(EthCoinHandler)
blockchain_handlers.register_class(BNBCoinHandler)
blockchain_handlers.register_class(ERC20Handler)
blockchain_handlers.register_class(ERC20HandlerRopsten)

# Map coins to handlers
blockchain_handlers.map_coins_to_handlers()
