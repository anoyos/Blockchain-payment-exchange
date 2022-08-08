import json
from datetime import datetime
from api_contrib.core.utils import CustomEncoder
import pytest

from app.api.internal.tools import process
from app.balance import transaction, trade, lock
from decimal import Decimal

BASE_TRADE = {
    'create_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'symbol': 'XLTtBTC',
    'price': Decimal('0.005'),
    'quantity': Decimal('3'),
    'value': Decimal('0.015'),
    'commission': Decimal('0.00003'),
    'base_currency_id': '0d8c6130-c2f8-42c3-afb4-a0be021aafcd',
    'base_currency_code': 'XLT',
    'quote_currency_id': '61ac9609-1ddd-4890-bfde-ac2929b7344f',
    'quote_currency_code': 'tBTC'
}

BUY_TRADE = dict(**BASE_TRADE)
SELL_TRADE = dict(**BASE_TRADE)

BUY_TRADE.update({
    'id': '60898c95b2d42c89121223e0',
    'side': 'BUY',
    'user_id': 'test_user'
})

SELL_TRADE.update({
    'id': '60898c95b2d42c89121223e1',
    'side': 'SELL',
    'user_id': 'test_user'
})


class TestTrade:
    @pytest.mark.parametrize("mock_trade", [SELL_TRADE])
    def test_change_balance_from_trade(self, mock_trade):
        message = json.dumps(mock_trade, cls=CustomEncoder)
        result = process(trade.apply, message)
        assert result['status'], 'success'


class TestTransaction:
    def test_change_balance_from_tran(self):
        message = json.dumps({
            "user_id": "test_user_id",
            "asset_id": "61ac9609-1ddd-4890-bfde-ac2929b7344f",
            "asset_code": "tBTC",
            "address": "test_deposit_address",
            "amount": 10,
            "tx_id": "test_tran_id",
            "status": "confirmed",
            "transaction_type": "deposit",
            "create_date": datetime.now().isoformat()
        })
        result = process(transaction.apply, message)
        assert result['status'] == 'success'


class TestLock:
    def test_lock_balance(self):
        # message =
        message = json.dumps({
            "user_id": "test_user_id",
            "asset_id": "61ac9609-1ddd-4890-bfde-ac2929b7344f",
            "address": "test_deposit_address",
            "amount": 10
        })
        result = process(lock.apply, message)
        assert result['status'] == 'success'
