from api_contrib.schemas.base import ResponseFormat
from pydantic import Field


class TextResponse(ResponseFormat):
    message: str = Field(description='Simple text about result of operation')
