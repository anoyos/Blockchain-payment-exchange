from assertpy import assert_that
from requests import post

from tests.utils import super_user
from tests.utils.admin_service_requests.add_market import add_market
from tests.utils.admin_service_requests.update_market_settings import update_market_setting
from tests.utils.auth_user import login_user, register_user, verify_registration
from tests.utils.services import all_markets_url


def test_get_all_markets_returns_markets():
    market_test_user = "markettestuser"
    super_user.delete_all()

    ### GIVEN
    token = register_user(market_test_user, "getmarketsuser@test.com")
    verify_registration(token)
    super_user.make_me_admin(market_test_user)
    auth_token = login_user("getmarketsuser@test.com")

    market_id = add_market(1, 2, auth_token)
    update_market_setting(market_id, "market_visible", True, auth_token)

    ### WHEN
    response = post(all_markets_url)

    ### THEN
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json()['status']).is_equal_to('success')
    markets = response.json().get('message')
    assert_that(markets).is_type_of(list)
    assert_that(markets).is_length(1)

    market = markets[0]
    assert_that(market['market_id']).is_equal_to(market_id)
    assert_that(market['base_asset_id']).is_equal_to(1)
    assert_that(market['asset_id']).is_equal_to(2)
    assert_that(market['market_name']).is_equal_to("DOGE-BTC")
    assert_that(market['price']).is_equal_to("0.00000000")
    assert_that(market['price_24']).is_equal_to("0.00000000")
    assert_that(market['high_24']).is_equal_to("0.00000000")
    assert_that(market['low_24']).is_equal_to("0.00000000")
    assert_that(market['change_24']).is_equal_to("0.00%")
    assert_that(market['volume_24']).is_equal_to("0.0000")
    assert_that(market['currentbid']).is_equal_to("0.00000000")
    assert_that(market['currentask']).is_equal_to("0.00000000")
    assert_that(market['visible']).is_equal_to(True)
    assert_that(market['featured']).is_equal_to(False)

