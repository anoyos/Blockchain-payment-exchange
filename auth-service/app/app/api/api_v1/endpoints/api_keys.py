import secrets
from typing import Any

from fastapi import APIRouter
from fastapi import Depends

from app import schemas, crud
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.ApiKeyResp)
async def get_full_profile(current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Returns user api keys
    """
    api_keys = await crud.api_key.find_all({"user_id": current_user.id, "status": "ACTIVE"})
    return {
        "message": api_keys
    }


@router.post("/create/", response_model=schemas.ApiKeyResp)
async def get_full_profile(current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Create api key for user
    """
    api_key = schemas.ApiKeyCreate(
        secret=secrets.token_urlsafe(32),
        user_id=current_user.id,
    )
    api_key.id = await crud.api_key.insert_one(api_key)
    return {
        "message": [api_key.dict()]
    }
