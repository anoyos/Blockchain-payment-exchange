from app.core.tools import settings


class TransactionStatus:
    NEW = 'NEW'
    PROCESSED = 'PROCESSED'


class AddressStatus:
    USED = 'USED'
    UNUSED = 'UNUSED'


class KeyScanStatus:
    NEW = 'NEW'
    SCANNED = 'SCANNED'


SERVICE_BTC_ADDRESS = '2MtR4utLzFLNXZ99BMkjc1imEwhvsZBvfvz'


def get_base_asset():
    for asset_code, asset_data in settings.ASSETS.items():
        if asset_data['is_quote_asset']:
            return asset_data
