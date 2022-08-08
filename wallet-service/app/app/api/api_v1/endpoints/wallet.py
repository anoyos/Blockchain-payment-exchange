from typing import Dict, Any

from api_contrib.core.services import get_current_user
from api_contrib.schemas import base as common_schemas
from fastapi import APIRouter, Depends, Path

from app import crud

router = APIRouter()


@router.post("/favorite/get/", response_model=common_schemas.FavoritesList)
async def get_favorite(user: Dict = Depends(get_current_user)) -> Any:
    """ Get user's favorites assets  """
    result_set = await crud.favorites_assets.find_all({"user_id": user['id']})
    return {
        'message': [row['asset_id'] for row in result_set]
    }


@router.post("/favorite/{asset_id}/{action}/", response_model=common_schemas.TextResponse)
async def update_favorite(user: Dict = Depends(get_current_user),
                          asset_id: str = Path(...),
                          action: str = Path(...)) -> Any:
    """ Add/Remove asset from favorites """
    query = {
        'asset_id': asset_id,
        'user_id': user['id']
    }
    if action == common_schemas.FavoritesAction.ADD:
        await crud.favorites_assets.create(query)
    if action == common_schemas.FavoritesAction.REMOVE:
        await crud.favorites_assets.delete_one(query)

    return common_schemas.TextResponse(message='SUCC_UPDATED')
