from typing import Dict, Any
from api_contrib.schemas.base import ResponseStatus
from api_contrib.schemas.base import TextResponse
from fastapi import APIRouter, Depends, HTTPException

from app import schemas, crud
from app.blockchain.handlers.factory import blockchain_handlers
from app.core.tools import get_asset_by_id
from app.models.wallet import TransactionStatus
from app.schemas.internal import LockBalanceMessage, ApplyTransactionMessage
from api_contrib.core.services import auth_user_with_mfa


router = APIRouter()


@router.post("/get_coin_tx_fees/")
async def get_usd_value() -> Any:
    """  Return tx fees for all coins """

    db_data = await crud.tx_fees.find_one({})

    return {"status": "success", 'message': db_data['data']}


@router.post("/get_commission/", response_model=schemas.CommissionResponse)
def get_withdrawal_commission(payload: schemas.CommissionRequest) -> Any:
    """
    Calc estimated fee for transaction
    """
    currency = get_asset_by_id(payload.asset_id)
    asset_code = currency['short_name']

    with blockchain_handlers.get(asset_code) as handler:
        fee = handler.calc_fee(payload.amount)

    return schemas.CommissionResponse(
        message=schemas.CommissionScheme(
            estimated_fee=fee))


@router.post("/", response_model=TextResponse)
async def withdrawal_confirm(payload: schemas.WithdrawalRequest,
                             user: Dict = Depends(auth_user_with_mfa),
                             ) -> Any:
    """
    Confirm withdrawal operation
        WD flow
        Request:
            1) WD req: user, asset, amount
            2) Calc commission in via bitcoinlib
            3) Check does balance sufficient for decrease if WD amount + commission
               a) If not - send message to user.
               b) If yes - send info to user.
    Confirm
            4) Send transaction to blockchain
    """

    # Prepare incoming data
    payload.user_id = user['id']
    payload.asset_code = get_asset_by_id(payload.asset_id)['short_name']

    # Save input operation
    withdrawal_record = await crud.transaction.create(payload.dict(), return_model=True)
    transaction_status = TransactionStatus.IN_PROCESS

    # Init blockchain handler
    with blockchain_handlers.get(payload.asset_code) as handler:
        # Calc commission, if not exists in incoming request
        if not withdrawal_record.commission:
            withdrawal_record.commission = handler.calc_fee(withdrawal_record.amount)

        # Try to freeze balance
        lock_message = LockBalanceMessage(**withdrawal_record.dict())
        locked_status = lock_message.send()

        # If no sufficient funds -  don't go next and say about it
        if locked_status.status == ResponseStatus.ERROR:
            await crud.transaction.set_status(withdrawal_record, ResponseStatus.ERROR)
            raise HTTPException(status_code=400, detail="Insufficient funds")

        # If balance is locked - send transaction to blockchain
        tx_id = handler.send_withdrawal_transaction(withdrawal_record)

        # Send decrease balance message
        if tx_id:
            withdrawal_record.tx_id = tx_id
            apply_message = ApplyTransactionMessage(**withdrawal_record.dict())
            result = apply_message.send()
            transaction_status = TransactionStatus.DONE if result.status == ResponseStatus.SUCCESS else \
                TransactionStatus.ERROR

        # Update operation status
        await crud.transaction.update(withdrawal_record, {
            "status": transaction_status,
            "commission": withdrawal_record.commission,
            "tx_id": withdrawal_record.tx_id
        })

    return {
        "message": transaction_status
    }
