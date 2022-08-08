from typing import Dict, Any

from api_contrib.core.services import get_current_user
from fastapi import APIRouter, Depends

from app import crud
from app import schemas

router = APIRouter()


@router.post("/deposits/", response_model=schemas.DepositResponse)
async def get_deposits(user: Dict = Depends(get_current_user)) -> Any:
    """
    Object with all user's completed deposit operations.
    """
    return {
        "message": await crud.deposit.find_all({
            "user_id": user["id"]
        })
    }


@router.post("/withdrawals/", response_model=schemas.WithdrawalResponse)
async def get_withdrawals(user: Dict = Depends(get_current_user)) -> Any:
    """
    Object with all user's completed withdrawals operations.
    """
    return {
        "message": await crud.withdrawal.find_all({
            "user_id": user["id"]
        })
    }
