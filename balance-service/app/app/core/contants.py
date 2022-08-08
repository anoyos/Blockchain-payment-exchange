from api_contrib.core.utils import logger

from app.core.config import settings
import json

with open(settings.ASSET_CONFIG_PATH) as fp:
    assets_raw = json.load(fp)
    assets = dict([(v['asset_id'], v) for k, v in assets_raw.items()])

logger.info(f"assets load from markets services: {len(assets)}")

BASE_ASSET = [value for key, value in assets.items() if value['is_base_asset']][0]


def get_asset_meta(asset_id: str) -> dict:
    assets_meta = assets[asset_id]

    return {
        'currency': assets_meta['short_name'],
        'currencyname': assets_meta['long_name']
    }
