from app import crud
from app.stat.prices import update_btc_price


def test_update_btc_price():
    db_data_before = crud.last_prices.find_one_sync({})
    update_time_before = 0 if not db_data_before else db_data_before['last_update_time'].timestamp()

    update_btc_price()

    db_data_after = crud.last_prices.find_one_sync({})
    update_time_after = 0 if not db_data_after else db_data_after['last_update_time'].timestamp()

    assert update_time_after > update_time_before



