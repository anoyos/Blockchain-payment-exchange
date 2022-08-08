auth_service = "http://localhost:5000"
websocket_url = "http://localhost:5001"
wallet_service = "http://localhost:5002"
balance_service = "http://localhost:5003"
market_service = "http://localhost:5005"
admin_service = "http://localhost:5007"
trollbox_service = "http://localhost:5010"

## ADMIN SERVICE
add_market_url = f"{admin_service}/api/v1/a/market/add/"
update_market_setting_url = f"{admin_service}/api/v1/a/market/set/"
add_trollbox_room = f"{admin_service}/api/v1/a/trollbox/rooms/"

## AUTH SERVICE
get_profile = f"{auth_service}/api/v1/user/profile/"
login_url = f"{auth_service}/api/v1/user/login/"
logout_url = f"{auth_service}/api/v1/user/logout/"
referral_codes_url = f"{auth_service}/api/v1/user/referralcode/"
register_url = f"{auth_service}/api/v1/user/onboarding/register/"
verify_registration_url = f"{auth_service}/api/v1/user/onboarding/verify/"

# BALANCE SERVICE
all_deposits_url = f"{balance_service}/api/v1/balance/deposits/"
all_withdrawals_url = f"{balance_service}/api/v1/balance/withdrawals/"
balances_url = f"{balance_service}/api/v1/balance/balances/"

## MARKET SERVICE
all_markets_url = f"{market_service}/api/v1/market/all/"
base_assets_url = f"{market_service}/api/v1/market/baseassets/"
assets_url = f"{market_service}/api/v1/market/assets/"

## TROLLBOX SERVICE
trollbox_rooms = f"{trollbox_service}/api/v1/trollbox/rooms/"
def new_trollbox_message(room_id) -> str:
    return f"{trollbox_service}/api/v1/trollbox/rooms/{room_id}/messages/"
def delete_trollbox_message(room_id, message_id):
    return f"{trollbox_service}/api/v1/trollbox/rooms/{room_id}/messages/{message_id}/"

## WALLET SERVICE
get_deposit_address_url = f"{wallet_service}/api/v1/currency/depositaddress/"

