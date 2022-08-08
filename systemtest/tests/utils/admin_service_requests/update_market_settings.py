from assertpy import assert_that
from requests import post

from tests.utils.auth_user import get_header_with_token
from tests.utils.services import update_market_setting_url


def update_market_setting(market_id, setting_name, setting_value, auth_token):
    payload = {
        "market_id": market_id,
        "setting": setting_name,
        "value": setting_value
    }
    headers = get_header_with_token(auth_token)
    response = post(update_market_setting_url, payload, headers=headers)

    assert_that(response.status_code, "Posting new market should be OK").is_equal_to(200)
    assert_that(response.json().get('status')).is_equal_to("success")
    assert_that(response.json().get('message')).is_equal_to("SUCC_UPDATED")
