from .base import CommonConfig, Transaction


class Deposit(Transaction):
    class Config(CommonConfig):
        collection_name = "deposit"
