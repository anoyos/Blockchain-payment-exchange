from typing import Any, Dict

from fastapi import APIRouter, Depends

from app import crud
from api_contrib.core.services import check_admin_permission

router = APIRouter()


@router.post("/list")
async def get_user_list_profile(user: Dict = Depends(check_admin_permission)) -> Any:
    """
    Get full the user's list.
    """
    markets = await crud.market.find_all({})
    total = len(markets)
    return {
        "status": 'success',
        "message": {
            "page": 1,
            "pages": 1,
            "perpage": total,
            "total_items": total,
            "items": markets
        }
    }

