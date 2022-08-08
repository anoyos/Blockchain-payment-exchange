from typing import Any

from fastapi import APIRouter, Depends

from app import crud
from app import schemas
from app.api import deps

router = APIRouter()


@router.post("/list")
async def get_user_list_profile(current_user: schemas.UserInDb = Depends(deps.get_user_admin_permissions)) -> Any:
    """
    Get full the user's list.
    """
    users = await crud.user.find_all({})
    total = len(users)
    return {
        "status": 'success',
        "message": {
            "page": 1,
            "pages": 1,
            "perpage": total,
            "total_items": total,
            "items": users
        }
    }


@router.post("/count")
async def get_user_list_profile(current_user: schemas.UserInDb = Depends(deps.get_user_admin_permissions)) -> Any:
    """
    Get full the user's list.
    """
    total = await crud.user.count()
    return {
        "status": 'success',
        "message": total
    }
