from assertpy import assert_that

from tests.utils import super_user
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import WALLET_QUEUE


class TestSaveNewAdresses:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()


    def test_save_new_addresses(self):
        # GIVEN
        celery = make_celery()
        addresses = [
            {
                'wallet_id': 'btcx',
                'address': 'address1'
            },
            {
                'wallet_id': 'btcx',
                'address': 'address2'
            }
        ]

        # WHEN
        result = celery.signature("wallet.save_new_addresses", [1, addresses]) \
            .set(queue=WALLET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_equal_to(f"{len(addresses)} new addresses saved to asset 1")