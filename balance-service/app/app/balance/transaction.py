from datetime import datetime
from decimal import Decimal

from app import crud
from app.core.contants import get_asset_meta
from app.models import AccountTypes
from app.models.deposit import Deposit
from app.models.withdrawal import Withdrawal
from .base.operations import increment_account_balance


def define_balance_increment(message: dict) -> dict:
    if message['transaction_type'] == 'deposit':
        amount = Decimal(message['amount'])
        return {
            'balance': amount,
            'available': amount,
            'locked': 0
        }
    elif message['transaction_type'] == 'withdrawal':
        balance_increment = Decimal(-1) * (Decimal(message['amount']) + Decimal(message.get('commission', 0)))

        return {
            'balance': balance_increment,
            'locked': balance_increment
        }


def save_incoming_operations(message: dict) -> None:
    if message['transaction_type'] == 'deposit':
        validated_deposit_obj = Deposit(
            user_id=message['user_id'],
            asset_id=message['asset_id'],
            asset_code=message['asset_code'],
            amount=message['amount'],
            address=message['address'],
            tx_id=message['tx_id'],
            transaction_time=message['create_date'],
            applied_time=datetime.now()
        )
        _ = crud.deposit.insert_one_sync(validated_deposit_obj)
    elif message['transaction_type'] == 'withdrawal':
        validated_withdrawal_obj = Withdrawal(
            user_id=message['user_id'],
            asset_id=message['asset_id'],
            asset_code=get_asset_meta(message['asset_id'])['currency'],
            amount=message['amount'],
            address=message['address'],
            tx_id=message['tx_id'],
            transaction_time=message['create_date']
        )

        _ = crud.withdrawal.insert_one_sync(validated_withdrawal_obj)


def apply(message):
    # Create records if not exists
    account_query = crud.balance.get_or_create_sync(query={
        'user_id': message['user_id'],
        'asset_id': message['asset_id'],
        'asset_code': message['asset_code']
    })
    system_spend_account = crud.balance.get_or_create_sync(query={
        'account_type': AccountTypes.SPEND,
        'asset_code': message['asset_code'],
        'asset_id': message['asset_id'],
        'user_id': 'bookeeper'
    })

    # Update balances values
    increment_values = define_balance_increment(message)

    if increment_values:
        save_incoming_operations(message)

        for account, increment in [
            (account_query, increment_values),
            (system_spend_account, increment_values)
        ]:
            increment_account_balance(account,
                                      increment,
                                      event_type=message['transaction_type'],
                                      event_id=message['tx_id'])
