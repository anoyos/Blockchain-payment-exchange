from typing import List

from bullflag_commons.exception import BullflagException
from bullflag_commons.logging import get_logger
from bullflag_connector_dummies.v2.market import MarketCeleryProducer

from app.service.wallet_service import WalletService


class MarketService:
    logger = get_logger(__name__)

    def __init__(self, market_celery_producer: MarketCeleryProducer, assets: List[dict]):
        self._market_celery_producer = market_celery_producer
        self._assets = assets

    def create_market(self, base_asset_id, asset_id) -> str:
        try:
            base_asset = next((item for item in self._assets if item["id"] == base_asset_id), None)
            asset = next((item for item in self._assets if item["id"] == asset_id), None)
        except BullflagException as bf_exec:
            self.logger.error('Could not find assets while creating markets: {}.'.format(bf_exec.message))
            raise bf_exec
        if base_asset and asset and (base_asset['is_base_asset'] and not asset['is_base_asset']):
            market_id = self._do_create(base_asset, asset)
            self.logger.info("Created new market: {}".format(market_id))
        else:
            message = "Bad combo of base/not-base assets: {}, {}." \
                .format(base_asset, asset)
            self.logger.error(message)
            raise BullflagException(message)

        return market_id

    def update_market_setting(self, setting):
        return self._market_celery_producer.market_update_setting(setting)

    def _do_create(self, base_asset, asset):
        market_data = {
            'base_asset_id': base_asset['id'],
            'asset_id': asset['id']
        }
        return self._market_celery_producer.add_market(market_data)
