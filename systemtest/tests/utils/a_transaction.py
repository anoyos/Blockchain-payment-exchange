# noinspection PyPep8Naming
class aTransaction:

    def __init__(self):
        self.transaction_type = 1
        self.timestamp_execution = 1000
        self.user_id = None
        self.amount = 10.5
        self.asset_id = 1
        self.metadata = {
            'txid': 'abc123',
            'address': 'wallet_address_1'
        }

    def with_transaction_type(self, transaction_type):
        self.transaction_type = transaction_type
        return self

    def with_ts_exec(self, ts_exec):
        self.timestamp_execution = ts_exec
        return self

    def with_user_id(self, user_id):
        self.user_id = user_id
        return self

    def with_amount(self, amount):
        self.amount = amount
        return self

    def with_asset_id(self, asset_id):
        self.asset_id = asset_id
        return self

    def with_metadata(self, metadata):
        self.metadata = metadata
        return self

    def to_dict(self):
        return {
            'transaction_type': self.transaction_type,
            'timestamp_execution': self.timestamp_execution,
            'amount': self.amount,
            'asset_id': self.asset_id,
            'metadata': self.metadata
        }
