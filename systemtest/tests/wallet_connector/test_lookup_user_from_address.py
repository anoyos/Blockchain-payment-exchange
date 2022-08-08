from assertpy import assert_that

from tests.utils import super_user, auth_user
from tests.utils.wallet_service_requests import requests
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import WALLET_QUEUE


class TestLookupUserFromAddress:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_user_has_address_when_lookup_user_from_address_then_success(self):
        # GIVEN
        celery = make_celery()
        userid, address, wallet_id = self._login_and_get_userid_address_wallet_id()

        # WHEN
        result = celery.signature("wallet.lookup_user_from_address", [wallet_id, address]) \
            .set(queue=WALLET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_not_empty()
        assert_that(result).is_equal_to(userid)

    def test_given_user_has_no_address_when_lookup_user_from_address_then_no_result(self):
        # GIVEN
        celery = make_celery()
        address = {
                'wallet_id': 'btcx',
                'address': 'address1'
            }

        # WHEN
        result = celery.signature("wallet.lookup_user_from_address", [address['wallet_id'], address['address']]) \
            .set(queue=WALLET_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_none()

    def _login_and_get_userid_address_wallet_id(self) -> (str, str, str):
        asset_id = 1
        token = auth_user.create_nonadmin_and_login("testuser", "testuser@mail.com")
        response = requests.get_deposit_address(asset_id, token)
        address = response.json().get("message").get("address")
        userid = super_user.get_userid("testuser")
        wallets = super_user.get_wallets_by_userid_and_asset_id(userid, asset_id)
        # fetch any wallet_id
        wallet_id = wallets[0]['wallet_id']
        return userid, address, wallet_id
