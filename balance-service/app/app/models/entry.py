from typing import Optional

from api_contrib.models import description, base
from pydantic import Field

from .base import CommonConfig


class Entry(base.MongoDbModel):
    event_date: str = Field(description="Date when event processed by balance worker")
    event_type: str = Field(description="Type of operation triggered balance changes")
    asset_code: str = Field(description=description.ASSET_ID)
    account_id: str = Field(description="Id of account")

    items: Optional[list] = Field(description="Array of events", default=[])

    class Config(CommonConfig):
        collection_name = "entry"
