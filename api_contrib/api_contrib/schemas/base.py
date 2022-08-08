from pydantic import BaseModel
from typing import Any


class ResponseFormat(BaseModel):
    status: str = 'success'
    message: Any
