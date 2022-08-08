from typing import Dict, List

from api_contrib.schemas.base import ResponseFormat

from app.models.asset import Asset


class AssetsArrayResponse(ResponseFormat):
    message: Dict[str, Asset]


class AssetsListResponse(ResponseFormat):
    message: List[Asset]


class FavoritesResponse(ResponseFormat):
    message: List[str]
