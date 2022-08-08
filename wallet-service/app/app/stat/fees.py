from app.blockchain.handlers.factory import blockchain_handlers
from app import crud


def update_withdrawal_fee():
    coin_fees = {}
    for asset_code in blockchain_handlers.handlers:
        handler = blockchain_handlers.get(asset_code)
        coin_fees[asset_code] = handler.estimate_fee()

    obj_with_new_values = {'data': coin_fees}
    fees = crud.tx_fees.get_or_create_sync(query={}, obj_data=obj_with_new_values)
    crud.tx_fees.update_sync(fees, obj_with_new_values)

