from assertpy import assert_that
from requests import post

from tests.utils import super_user
from tests.utils.auth_user import get_header_with_token, create_admin_and_login, create_nonadmin_and_login
from tests.utils.services import add_market_url

payload_good_pair = {
    "base_asset_id": 1,
    "asset_id": 2
}

payload_bad_pair = {
    "base_asset_id": 3,
    "asset_id": 2
}


class TestAddMarket:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_admin_when_adding_market_then_works(self):
        # GIVEN
        token = create_admin_and_login("adminuser")
        headers = get_header_with_token(token)

        # WHEN
        response = post(add_market_url, payload_good_pair, headers=headers)

        # THEN
        assert_that(response.status_code, "Posting new market should be OK").is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to("success")
        market_id = response.json().get('message').get('market_id')
        assert_that(market_id, "Market id is returned").is_not_empty()

    def test_given_not_admin_when_adding_market_then_fails(self):
        # GIVEN
        non_admin_token = create_nonadmin_and_login("nonadmin")
        headers = get_header_with_token(non_admin_token)

        # WHEN
        response = post(add_market_url, payload_good_pair, headers=headers)

        # THEN
        assert_that(response.status_code, "Posting new market should be OK").is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to("fail")
        assert_that(response.json().get('message')).is_equal_to("ERR_INVALID_REQUEST")

    def test_given_no_base_asset_when_adding_market_then_fails(self):
        # GIVEN
        admin_token = create_admin_and_login("adminuser")

        # WHEN
        headers = get_header_with_token(admin_token)
        response = post(add_market_url, payload_bad_pair, headers=headers)

        # THEN
        assert_that(response.status_code, "Posting new market should be OK").is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to("fail")
        markets_erroring = ("{'id': 3, 'short_name': 'MLN', 'long_name': 'Melonhead Protocol', 'is_base_asset': False, 'decimal_precision': 8}, "
                            "{'id': 2, 'short_name': 'DOGE', 'long_name': 'Dogecoin', 'is_base_asset': False, 'decimal_precision': 6}")
        assert_that(response.json().get('message')).is_equal_to("Bad combo of base/not-base assets: {}.".format(markets_erroring))

    def test_given_market_exists_when_adding_same_market_again_then_fails(self):
        # GIVEN
        token = create_admin_and_login("adminuser")
        headers = get_header_with_token(token)
        response = post(add_market_url, payload_good_pair, headers=headers)

        # WHEN
        second_response = post(add_market_url, payload_good_pair, headers=headers)

        # THEN
        assert_that(response.status_code, "Posting new market should be OK").is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to("success")

        assert_that(second_response.json().get('status')).is_equal_to("fail")
        expected_message = self._expected_message("1", "2")
        assert_that(second_response.json().get('message')).is_equal_to(expected_message)

    def _expected_message(self, base_asset_id, asset_id):
        return "Market exists already for {{'base_asset_id': {}, 'asset_id': {}}}".format(
            base_asset_id, asset_id)
