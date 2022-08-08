from typing import Optional

from api_contrib.schemas.base import ResponseFormat
from pydantic import BaseModel


class Msg(BaseModel):
    msg: str


class IdResponse(BaseModel):
    id: str


class NewRecord(ResponseFormat):
    message = IdResponse


class Token(ResponseFormat):
    message: str = "SUCCESS_LOGGED_IN"
    auth_token: str
    access_token: str
    userid: str
    refresh_token: Optional[str] = None
    token: Optional[str] = None
    expires_at: int
    servertime: int


class ConfirmToken(BaseModel):
    token: str


class RefreshToken(BaseModel):
    refresh_token: str
