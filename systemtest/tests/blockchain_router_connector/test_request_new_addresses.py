from assertpy import assert_that

from tests.utils import super_user
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BLOCK_CHAIN_ROUTER_QUEUE


class TestRequestNewAddresses:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_request_new_addresses(self):
        # GIVEN
        celery = make_celery()

        # WHEN
        # 1 = asset, 3 = amount of new addresses to request
        result = celery.signature('blockchain_router.request_new_addresses', [1, 3]) \
            .set(queue=BLOCK_CHAIN_ROUTER_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(len(result)).is_equal_to(3)

        assert_that(result[0]['wallet_id']).is_equal_to("btc_1")
        assert_that(result[0]['address']).contains("wallet-address-")

        assert_that(result[1]['wallet_id']).is_equal_to("btc_1")
        assert_that(result[1]['address']).contains("wallet-address-")

        assert_that(result[2]['wallet_id']).is_equal_to("btc_1")
        assert_that(result[2]['address']).contains("wallet-address-")
