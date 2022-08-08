from decimal import Decimal

from app import crud
from .base.operations import increment_account_balance


class NoBalanceFoundException(Exception):
    def __str__(self):
        return "No balance found"


class NoSufficientFundsException(Exception):
    def __str__(self):
        return "No sufficient funds"


def apply(request):
    """
    Locked account value
    """
    # Prepare values
    query = {
        'user_id': request['user_id'],
        'asset_id': request['asset_id']
    }
    value_for_lock = Decimal(request['amount']) + Decimal(request.get('commission', 0))
    account = crud.balance.find_one_sync(query)

    # Exit if account found
    if not account:
        raise NoBalanceFoundException

    # Check if account is sufficient for lock
    new_available_value = account['available'] - value_for_lock
    if new_available_value < 0:
        raise NoSufficientFundsException

    # locked value of account
    increment_account_balance(account, {
        "account": 0,
        "available": Decimal(-1) * value_for_lock,
        "locked": value_for_lock,
    }, push_entry=False)
