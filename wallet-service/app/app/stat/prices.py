import requests
from datetime import datetime
from app import crud
from app.models.wallet import LastPrices
from app.core import constants


def filter_fiat_prices(api_data: dict) -> dict:
    fiat_currency_list = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'CHF', 'CNY', 'NZD', 'JPY']
    result = {}
    for code in fiat_currency_list:
        if code.lower() in api_data:
            result[code] = api_data[code.lower()]
    return result


def get_current_prices() -> dict:
    url = 'https://api.coingecko.com/api/v3/coins/bitcoin?localization=false&' \
          'tickers=false&community_data=false&developer_data=false&sparkline=false'
    data = requests.get(url).json()['market_data']['current_price']
    return data


def get_base_asset_constant() -> dict:
    base_asset = constants.get_base_asset()
    return {
        base_asset['short_name']: '1.00000000',
        'asset_id': base_asset['asset_id'],
        'short_name': base_asset['short_name'],
    }


def update_btc_price() -> None:
    """
    Scheduled task to periodically take BTC price from other exchanges, and save current BTC price
    into different fiat currencies.
    Document stored in API response for UI:

    :return:
    """
    # Take data from API
    external_data = get_current_prices()
    #
    asset_data = get_base_asset_constant()
    fiat_prices = filter_fiat_prices(external_data)

    asset_data.update(fiat_prices)

    current_data = crud.last_prices.find_one_sync({})
    if current_data:
        crud.last_prices.update_sync(current_data, {"prices": asset_data,
                                                    "last_update_time": datetime.now()})
    else:
        obj = LastPrices(prices=asset_data)
        crud.last_prices.insert_one_sync(obj)


if __name__ == '__main__':
    update_btc_price()
