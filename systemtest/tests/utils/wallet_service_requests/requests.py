from requests import post

from tests.utils.auth_user import get_header_with_token
from tests.utils.services import get_deposit_address_url


def get_deposit_address(asset_id: int, auth_token: str):
    """
    Gets a deposit address for authenticated user
    :return: response payload
    """
    headers = get_header_with_token(auth_token)

    payload = {
        "asset_id": asset_id
    }

    return post(get_deposit_address_url, payload, headers=headers)
