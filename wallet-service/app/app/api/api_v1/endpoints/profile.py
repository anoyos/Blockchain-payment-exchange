from typing import Any

from fastapi import APIRouter

from app import schemas, crud

router = APIRouter()


@router.post("/usdvalue/", response_model=schemas.UsdValuesList)
async def get_usd_value() -> Any:
    """  Retrieve all markets """

    db_data = await crud.last_prices.find_one({})

    return {"status": "success", 'message': [db_data['prices']]}
