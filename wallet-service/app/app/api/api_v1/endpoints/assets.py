from typing import Any

from fastapi import APIRouter

from app import crud, schemas

router = APIRouter()


@router.post("/assets/all/", response_model=schemas.AssetsListResponse)
async def get_all_assets() -> Any:
    """" Completed list of quote currencies, use as fiat money """
    return schemas.AssetsListResponse(message=await crud.asset.find_all({"listed": True}))
