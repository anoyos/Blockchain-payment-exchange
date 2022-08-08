from calendar import timegm
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException

from app import crud, schemas

router = APIRouter()


@router.post("/all/", response_model=schemas.MarketArrayResponse)
async def get_all_markets() -> Any:
    """ Returns all markets """
    return {
        "message": await crud.market.get_query_as_dict()
    }


@router.post("/", response_model=schemas.MarketArrayResponse)
async def get_market(payload: schemas.MarketFilter) -> Any:
    """ Returns market info by ID """
    market = await crud.market.find_one({"symbol": payload.symbol})
    if not market:
        raise HTTPException(status_code=404, detail="Market not found")
    return {
        "message": {
            market['id']: market
        }
    }


@router.post("/servertime/")
async def get_server_time() -> Any:
    """ Returns the server time """
    return {
        "status": 'success',
        "message": timegm(datetime.utctimetuple(datetime.now()))
    }
