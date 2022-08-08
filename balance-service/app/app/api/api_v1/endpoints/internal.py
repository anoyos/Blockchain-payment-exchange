from typing import Any

from api_contrib.core.services import reusable_oauth2
from api_contrib.schemas.base import UserIdRequest
from fastapi import APIRouter, Depends, HTTPException

from app import crud
from app.core.config import settings

router = APIRouter()


@router.post("/user/{collection_name}/", include_in_schema=False)
async def get_user_active_tokens(collection_name: str,
                                 payload: UserIdRequest,
                                 token: str = Depends(reusable_oauth2)
                                 ) -> Any:
    """
    Get user account data for internal services
    """

    if token != settings.CLUSTER_API_KEY:
        raise HTTPException(status_code=401, detail="Not authorized")

    if collection_name == 'deposits':
        return await crud.deposit.find_all({
            "user_id": payload.user_id
        })
    elif collection_name == 'withdrawals':
        return await crud.withdrawal.find_all({
            "user_id": payload.user_id
        })
    else:
        return await crud.balance.find_all({
            "user_id": payload.user_id
        })
