from decimal import Decimal

from app import crud
from app import models
from .base.operations import increment_account_balance


def apply(trade):
    """
    Trades:

    Ex1:
    who: user1
    type:  SELL
    what:  LTC
    quantity: 2
    price: 0.005 BTC

    Ex2:
    who: user2
    type:  BUY
    what:  LTC
    quantity: 2
    price: 0.005 BTC

    ========
    value = price * quantity
    commission = value * commission_percent
    ========
    BUY:
          asset account (ex. LTC) += (quantity  - commission)
          base account (ex.BTC) -= (value + commission)

    SELL:
          asset account (ex. LTC) -= (quantity + commission)
          base account (ex. BTC) += (value  - commission)

    Real Trade message

        trade = Trade(
        user_id=order.user_id,
        side=BUY,
        symbol=order.symbol,
        price=order.price,
        quantity=trade_size,
        value=trade_value,
        commission=commission,
        base_currency_id=market.quote_currency_id,
        base_currency_code=market.quote_currency_code,
        quote_currency_id=market.quote_currency_id,
        quote_currency_code=market.quote_currency_code
    )
    """
    # Get values from message
    user_id = trade['user_id']
    quantity = Decimal(trade['quantity'])
    commission = Decimal(trade['commission'])
    value = Decimal(trade['value'])

    # Define increment values
    if trade['side'] == 'BUY':
        base_currency_increment = quantity
        quote_currency_increment = -1 * value
    else:
        base_currency_increment = -1 * quantity
        quote_currency_increment = value

    # Take commission from base account
    quote_currency_increment -= commission

    # Get accounts
    base_currency_account = crud.balance.get_or_create_sync({
        'user_id': user_id,
        'asset_id': trade['base_currency_id'],
        'asset_code': trade['base_currency_code']
    })

    quote_currency_account = crud.balance.get_or_create_sync({
        'user_id': user_id,
        'asset_id': trade['quote_currency_id'],
        'asset_code': trade['quote_currency_code']
    })

    profit_account = crud.balance.get_or_create_sync({
        'account_type': models.AccountTypes.PROFIT,
        'asset_code': trade['quote_currency_code'],
        'asset_id': trade['quote_currency_id'],
        'user_id': 'bookeeper'
    })

    # Update balances values
    for account, increment in [
        (quote_currency_account, quote_currency_increment),
        (base_currency_account, base_currency_increment),
        (profit_account, commission),
    ]:
        increment_account_balance(account, {
                                        "balance": increment,
                                        "available": increment
                                  },
                                  event_type="trade",
                                  event_id=trade['id'])
