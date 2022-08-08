from assertpy import assert_that, fail

from tests.utils import super_user, auth_user
from tests.utils.admin_service_requests import add_market
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import MARKET_QUEUE

class TestAdd:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_new_market_when_add_market_then_success(self):
        # GIVEN
        celery = make_celery()
        payload = {
            "base_asset_id": 1,
            "asset_id": 2
        }

        # WHEN
        result = celery.signature("market.add", [payload]) \
            .set(queue=MARKET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_not_empty()
        assert_that(result).is_type_of(str)

    def test_given_existing_market_when_add_market_then_fails(self):
        # GIVEN
        celery = make_celery()
        payload = {
            "base_asset_id": 1,
            "asset_id": 2
        }

        token = auth_user.create_admin_and_login("adminuser")
        add_market.add_market(payload["base_asset_id"], payload["asset_id"], token)

        # WHEN
        result = ""
        try:
            result = celery.signature("market.add", [payload]) \
                .set(queue=MARKET_QUEUE) \
                .set(expires=1) \
                .delay() \
                .get(1)
            fail("should have raised error")
        except Exception as e:

            # THEN
            assert_that(e).is_type_of(Exception)
            assert_that(str(e)).is_equal_to("Market exists already for {'base_asset_id': 1, 'asset_id': 2}")


