from assertpy import assert_that

from tests.utils import super_user
from tests.utils.auth_user import create_nonadmin_and_login
from tests.utils.wallet_service_requests.requests import get_deposit_address

btc_asset = 1


class TestGetDepositAddress:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_user_when_get_deposit_address_then_it_is_returned(self):
        # GIVEN
        auth_token = create_nonadmin_and_login("userGetDepAddress")
        # WHEN
        response = get_deposit_address(btc_asset, auth_token)
        # THEN
        assert_that(response.status_code, "msg").is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to("success")
        assert_that(response.json().get('message').get('address')).contains("wallet-address-")
        assert_that(response.json().get('message').get('note')).contains("This is a - Bitcoin (BTC) - address.")

    def test_given_user_when_get_two_times_then_same_deposit_address_is_returned_both_times(self):
        # GIVEN
        auth_token = create_nonadmin_and_login("userGetDepAddress")
        # WHEN
        response1 = get_deposit_address(btc_asset, auth_token)
        response2 = get_deposit_address(btc_asset, auth_token)
        # THEN
        address1 = response1.json().get('address_something')
        address2 = response2.json().get('address_something')

        assert_that(address1).is_not_empty()
        assert_that(address2).is_not_empty()
        assert_that(address1).is_equal_to(address2)

    def test_given_two_users_when_get_deposit_address_then_they_get_one_each(self):
        # GIVEN
        auth_token_user_1 = create_nonadmin_and_login("depositaddruser1", "depositaddruser1@mail.com")
        auth_token_user_2 = create_nonadmin_and_login("depositaddruser2", "depositaddruser2@mail.com")

        # WHEN
        asset_btc = 1
        user1_response = get_deposit_address(asset_btc, auth_token_user_1)
        user2_response = get_deposit_address(asset_btc, auth_token_user_2)
        user1_address = user1_response.json().get('message').get('address')
        user2_address = user2_response.json().get('message').get('address')

        # THEN
        assert_that(user1_address).is_not_empty()
        assert_that(user2_address).is_not_empty()
        assert_that(user1_address).is_not_equal_to(user2_address)
