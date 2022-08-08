from app import crud
from app.core.config import settings
from app.core.constants import AddressStatus
from app.models.wallet import DepositAddresses

class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self

def clear_deposit_data(handler):
    handler.deposit_request = crud.deposit_addresses.find_one_sync({
        'address': handler.tran_address,
        'asset_code': handler.asset_code,
        'user_id': handler.mock_user['id']
    })
    if not handler.deposit_request:
        handler.deposit_request = crud.deposit_addresses.insert_one_sync(
            DepositAddresses(
                user_id=handler.mock_user['id'],
                address=handler.tran_address,
                currency_name=handler.asset_code,
                asset_code=handler.asset_code,
                asset_id=settings.ASSETS[handler.asset_code]['asset_id'],
            ), return_obj=True
        )

    else:
        crud.deposit_addresses.update_sync(handler.deposit_request, {
            'status': AddressStatus.UNUSED
        })

    crud.transaction.delete_one_sync({"tx_id": handler.test_tx_id})
