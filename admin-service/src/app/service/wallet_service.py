from bullflag_commons.exception import BullflagException
from bullflag_commons.logging import get_logger
from bullflag_connector_dummies.v2.wallet import WalletCeleryProducer


class WalletService:
    logger = get_logger(__name__)

    def __init__(self, wallet_celery_producer: WalletCeleryProducer):
        self._wallet_celery_producer = wallet_celery_producer

    def wallet_exists(self, currency_short_name) -> bool:
        wallet_exists = self._wallet_celery_producer.wallet_exists(currency_short_name)
        if wallet_exists:
            self.logger.info("Checking wallet exists, it did. {}".format(currency_short_name))
        return wallet_exists

    def create_new_wallet(self, currency_data) -> str:
        try:
            currency_id_from_new_wallet = self._wallet_celery_producer.create_new_wallet(currency_data)
            self.logger.info("Created new wallet: {}".format(currency_data))
            return currency_id_from_new_wallet
        except Exception as exec:
            self.logger.error("Creating new wallet {} failed: {}".format(currency_data, exec), exc_info=exec)

    def get_wallet_by_short_name(self, curr_short_name) -> dict:
        wallet_profiles = self._wallet_celery_producer.get_wallet_profile_all()
        for wallet_profile in wallet_profiles:
            if wallet_profile['currency_short_name'] == curr_short_name:
                return wallet_profile
        raise BullflagException("No wallet found for currency short name {}".format(curr_short_name))

    def update_wallet_setting(self, setting):
        return self._wallet_celery_producer.wallet_update_setting(setting)