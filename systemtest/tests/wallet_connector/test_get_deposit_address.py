from assertpy import assert_that

from tests.utils import super_user, auth_user
from tests.utils.wallet_service_requests import requests
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import WALLET_QUEUE


class TestGetDepositAddress:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_user_has_address_assigned_when_get_deposit_address_then_assigned_address_is_returned(self):
        # GIVEN
        celery = make_celery()
        userid, address = self._login_and_get_userid_address()

        # WHEN
        result = celery.signature("wallet.get_deposit_address", [{"asset_id": 1, "user_id": userid}]) \
            .set(queue=WALLET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_not_empty()
        assert_that(result).is_equal_to(address)

    def test_given_user_has_no_address_assigned_and_there_is_available_adresses_when_get_deposit_address_then_new_address_is_returned(self):
        # GIVEN
        celery = make_celery()
        self._login_and_get_userid_address()

        # WHEN
        result = celery.signature("wallet.get_deposit_address", [{"asset_id": 1, "user_id": "dummyID"}]) \
            .set(queue=WALLET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        #THEN
        assert_that(result).is_not_empty()
        assert_that(result).is_type_of(str)

    def test_given_user_has_no_address_assigned_and_there_is_no_available_adresses_when_get_deposit_address_then_none_is_returned(self):
        # GIVEN
        celery = make_celery()

        # WHEN
        result = celery.signature("wallet.get_deposit_address", [{"asset_id": 1, "user_id": "123_dummy_uuid"}]) \
            .set(queue=WALLET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_none()

    def _login_and_get_userid_address(self) -> str:
        asset_id = 1
        token = auth_user.create_nonadmin_and_login("testuser", "testuser@mail.com")
        response = requests.get_deposit_address(asset_id, token)
        address = response.json().get("message").get("address")
        userid = super_user.get_userid("testuser")
        return userid, address


