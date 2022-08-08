from uuid import uuid4

from requests import post, Response

from tests.utils.auth_user import get_header_with_token, create_admin_and_login
from tests.utils.services import add_wallet_url


# def add_wallet(currency_short_name: str, auth_token: str = None) -> Response:
#     """
#     Returns the http response object.
#
#     Parameters:
#         currency_short_name: Example "BTC"
#         auth_token: Needs to be token for admin user. If not supplied, admin user will be created.
#     """
#
#     if auth_token is None:
#         # currently, username needs to be max 30 chars and no dashes
#         auth_token = create_admin_and_login(str(uuid4()).replace('-', '')[:15])
#     payload = {
#         "currency_short_name": currency_short_name,
#         "currency_name": "{}-looong-name".format(currency_short_name),
#         "currency_type": "PoW",
#         "wallet_port_rpc": "123",
#         "wallet_port_p2p": "456",
#         "wallet_host": "localhost",
#         "username": "usr_name",
#         "password": "pwd",
#         "wpassword": "wpwd",
#         "wallet_host_backup": "host_backup",
#         "confirmations": "7",
#         "withdrawal_fee": "0.4"
#     }
#
#     headers = get_header_with_token(auth_token)
#
#     response = post(add_wallet_url, payload, headers=headers)
#
#     return response
#
# def add_wallet_return_currency_id(currency_short_name: str, auth_token: str = None):
#     return add_wallet(currency_short_name, auth_token).json()['payload']['currency_id']