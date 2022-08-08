from decimal import Decimal

from bson.decimal128 import Decimal128
from api_contrib.core.services import wallet_service
from app.models.balance import BalanceSettings


def to_dec128(value: str) -> Decimal128:
    return Decimal128(value)


def satoshi_to_btc(value: int) -> str:
    return f"{value / 100000000:.8f}"


def dec_to_str(value: Decimal) -> str:
    return f"{value:.8f}"


def merge_settings(asset_code: str, settings: dict) -> dict:
    tx_fees = wallet_service.send('withdraw/get_coin_tx_fees')
    fee = tx_fees[asset_code]
    if settings is None:
        return BalanceSettings(txfee=fee).dict()
    else:
        settings['txfee'] = fee
        return settings
