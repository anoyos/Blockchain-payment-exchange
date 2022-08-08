from calendar import timegm
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt

from app.core.config import Settings


def generate_confirm_token(settings: Settings, sub: str) -> str:
    delta = timedelta(minutes=settings.CONFIRM_TOKEN_MINUTES)
    now = datetime.utcnow()
    expires = now + delta
    exp = timegm(expires.utctimetuple())
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": sub}, settings.SECRET_KEY, algorithm="HS256",
    )
    return encoded_jwt


def verify_confirm_token(settings: Settings, token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError as e:
        raise e
