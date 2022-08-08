from typing import List, Dict

from api_contrib.schemas.base import ResponseFormat


class UsdValuesList(ResponseFormat):
    message: List[Dict]
