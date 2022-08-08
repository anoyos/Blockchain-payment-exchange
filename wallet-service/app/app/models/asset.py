from api_contrib.models.base import MongoDbModel
from typing import Optional
from .base import CommonConfig


class Asset(MongoDbModel):
    short_name: str
    long_name: str
    is_base_asset: bool
    is_quote_asset: Optional[bool] = False
    decimal_precision: int
    asset_id: str
    listed: Optional[bool] = False
    main_net_code: Optional[str]
    is_erc20: Optional[bool] = False
    token_contract: Optional[str]
    handler: str

    class Config(CommonConfig):
        collection_name = "assets"
