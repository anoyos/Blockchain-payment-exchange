from typing import Any, Dict

from fastapi import APIRouter, Path, Depends

from app import crud, schemas

from api_contrib.core.services import get_current_user

router = APIRouter()


@router.post("/favorite/get/", response_model=schemas.FavoritesResponse)
async def market_favorite(user: Dict = Depends(get_current_user)) -> Any:
    """" Markets ID user marked as favorites """
    rows = await crud.favorites.find_all({'user_id': user['id']})
    return schemas.FavoritesResponse(message=[item["market_id"] for item in rows])


@router.post("/favorite/{market_id}/{action}/", response_model=schemas.TextResponse)
async def update_favorite(user: Dict = Depends(get_current_user),
                          market_id: str = Path(...),
                          action: str = Path(...)) -> Any:
    """" Add/Remove market from favorites """
    query = {
        'market_id': market_id,
        'user_id': user['id']
    }
    if action == schemas.FavoritesAction.ADD:
        await crud.favorites.insert_one(crud.Favorites(**query))
    if action == schemas.FavoritesAction.REMOVE:
        await crud.favorites.delete_one(query)

    return schemas.TextResponse(message='SUCC_UPDATED')
