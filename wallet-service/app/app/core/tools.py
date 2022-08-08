from decimal import Decimal
from typing import Dict
from app.core.config import settings


def btc_to_satoshi(value: str) -> int:
    return int(Decimal(value) * Decimal(10 ** 8))


def satoshi_to_btc(value: Decimal) -> Decimal:
    return value/Decimal(10 ** 8)


def get_base_asset():
    assets = settings.ASSETS
    base_asset = [v for k, v in assets.items() if v['is_base_asset'] is True]
    return base_asset[0]['id'], base_asset[0]['short_name']


def get_asset_by_id(asset_id: str) -> Dict:
    asset = {}
    for k, v in settings.ASSETS.items():
        if v['asset_id'] == asset_id:
            return v
    return asset


def get_asset_id_by_code(asset_code: str) -> str:
    if asset_code in settings.ASSETS:
        return settings.ASSETS[asset_code]['asset_id']
    else:
        return asset_code



