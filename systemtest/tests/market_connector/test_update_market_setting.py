from uuid import uuid4

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

    def test_given_existing_market_when_update_market_settings_then_success(self):
        # GIVEN
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

        # WHEN
        before_state = execute_celery("market.get_market_all", [])
        execute_celery("market.update_market_setting", [market_setting])
        result = execute_celery("market.get_market_all", [])

        # THEN
        assert_that(before_state).is_equal_to([])
        assert_that(result).is_not_empty()
        assert_that(result[0]['visible']).is_equal_to(True)

    def test_given_non_existing_market_when_update_market_settings_then_fails(self):
        # GIVEN
        celery = make_celery()
        market_id = uuid4()
        market_setting = {
            "market_id": market_id,
            "setting": "market_visible",
            "value": True
        }

        # WHEN
        before_state = execute_celery("market.get_market_all", [])
        result = ""
        try:
            result = execute_celery("market.update_market_setting", [market_setting])
            fail("should have raised error")
        except Exception as e:

            # THEN
            assert_that(before_state).is_empty()
            assert_that(str(e)).is_equal_to(f"Update setting for market failed. market_id: {market_id}.")


def execute_celery(task_name, payload):
    celery = make_celery()
    return celery.signature(task_name, payload) \
        .set(queue=MARKET_QUEUE) \
        .set(expires=1) \
        .delay() \
        .get(1)