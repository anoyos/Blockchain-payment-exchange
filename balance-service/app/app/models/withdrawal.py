from .base import CommonConfig, Transaction


class Withdrawal(Transaction):
    class Config(CommonConfig):
        collection_name = "withdrawal"
