from assertpy import assert_that
from requests import post

from tests.utils.auth_user import get_header_with_token
from tests.utils.services import add_market_url


def add_market(base_asset_id: int, asset_id: int, auth_token: str):
    payload = {
        "base_asset_id": base_asset_id,
        "asset_id": asset_id
    }
    headers = get_header_with_token(auth_token)

    response = post(add_market_url, payload, headers=headers)
    market_id = response.json().get('message').get('market_id')

    assert_that(response.status_code, "Posting new market should be OK").is_equal_to(200)
    assert_that(market_id, "Market id is returned").is_not_empty()

    return market_id
