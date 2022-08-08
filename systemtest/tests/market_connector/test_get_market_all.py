from assertpy import assert_that

from tests.utils import super_user, auth_user
from tests.utils.admin_service_requests import add_market
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import MARKET_QUEUE

class TestGetMarketAll:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_market_exist_when_get_market_all_then_success(self):
        # GIVEN
        celery = make_celery()

        payload = {
            "base_asset_id": 1,
            "asset_id": 2
        }
        token = auth_user.create_admin_and_login("adminuser")
        market_id = add_market.add_market(payload["base_asset_id"], payload["asset_id"], token)
        market_setting = {
            "market_id": market_id,
            "setting": "market_visible",
            "value": True
        }
        execute_celery("market.update_market_setting", [market_setting])

        # WHEN
        result = execute_celery("market.get_market_all", [])
        # THEN
        assert_that(result).is_not_empty()
        assert_that(result).is_type_of(list)

    def test_given_market_not_exist_when_get_market_all_then_fails(self):
        # GIVEN
        celery = make_celery()

        # WHEN
        result = execute_celery("market.get_market_all", [])

        # THEN
        assert_that(result).is_empty()
        assert_that(result).is_type_of(list)


def execute_celery(task_name, payload):
    celery = make_celery()
    return celery.signature(task_name, payload) \
        .set(queue=MARKET_QUEUE) \
        .set(expires=1) \
        .delay() \
        .get(1)