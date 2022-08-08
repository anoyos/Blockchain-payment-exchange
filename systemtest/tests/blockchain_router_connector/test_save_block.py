from assertpy import assert_that

from tests.utils import super_user
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BLOCK_CHAIN_ROUTER_QUEUE


class TestSaveBlock:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_save_block(self):
        # GIVEN
        celery = make_celery()
        block_data = {
            'hash': 'block_hash_from_blockchain',
            'height': 1337
        }
        # args: [callback from celery-call-chain, asset_id, wallet_id, crypto-block-data]
        payload = ["returned from celery chain", 1, "some_crypto_wallet", block_data]

        # WHEN
        result = celery.signature('blockchain_router.save_block', payload) \
            .set(queue=BLOCK_CHAIN_ROUTER_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_equal_to("block_hash_from_blockchain")
