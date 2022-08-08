import time
from typing import List

from tests.utils.system import SYSTEM_UUID


def get_deposits_transactions(user_id) -> List[dict]:
    exec_time = time.time_ns()
    return [
        {
            'transaction_type': 1,
            'user_id': user_id,
            'timestamp_execution': exec_time,
            'asset_id': 1,
            'amount': 10.00000001,
            'metadata': {
                'txid': '1',
                'address': 'a'
            }
        }, {
            'transaction_type': 1000,
            'timestamp_execution': exec_time,
            'asset_id': 1,
            'amount': -10.00000001,
            'user_id': SYSTEM_UUID,
            'metadata': {
                'txid': 1,
                'address': 'a'
            }
        }
    ]


def get_withdrawal_transactions(user_id) -> List[dict]:
    exec_time = time.time_ns()
    return [
        {
            'transaction_type': 2,
            'user_id': user_id,
            'timestamp_execution': exec_time,
            'asset_id': 1,
            'amount': -10.00000001,
            'metadata': {
                'txid': '1',
                'to_address': 'a',
                'from_address': 'b'
            }
        }, {
            'transaction_type': 1000,
            'timestamp_execution': exec_time,
            'asset_id': 1,
            'amount': 10.00000001,
            'user_id': SYSTEM_UUID,
            'metadata': {
                'txid': '1',
            }
        }
    ]
