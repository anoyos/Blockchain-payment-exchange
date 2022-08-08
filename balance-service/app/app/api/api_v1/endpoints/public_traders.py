from fastapi import APIRouter

from app import crud

router = APIRouter()


def convert_asset(account):
    return {
        "asset_code": account['asset_code'],
        "invested": 11.99,
        "pl": 50.07,
        "value": round(account['balance'], 4),
        "buy": 52.73,
        "current": 100.73,
    }


@router.get("/portfolio")
async def get_public_portfolio(user_id: str):
    all_assets = await crud.balance.find_all({
        "user_id": user_id
    })

    return [
        convert_asset(asset) for asset in all_assets
    ]
