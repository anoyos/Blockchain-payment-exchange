from datetime import timedelta
from time import time
from typing import Any, Union

from api_contrib.schemas.base import TextResponse
from fastapi import APIRouter, Depends, Path

from app import schemas, crud
from app.api import deps
from app.core import security, config

router = APIRouter()


@router.post("/refresh/")
async def create_new_session(user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Refresh user session
    """
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return schemas.Token(
        auth_token=token,
        access_token=token,
        userid=user.id,
        expires_at=security.get_exp(token),
        servertime=int(time())
    )


@router.post("/list/", response_model=schemas.SessionListResponse)
async def get_sessions(user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Gets a list of user sessions
    """
    data = await crud.session.find_all({"user_id": user.id,
                                        "status": schemas.SessionStatus.ACTIVE
                                        })
    return {
        "message": [row for row in data]
    }


@router.post("/logout/{session_id}/", response_model=TextResponse)
async def logout_current_session(user: schemas.UserInDb = Depends(deps.get_current_user),
                                 session_id: Union[str, int] = Path(...)
                                 ) -> Any:
    """
    Close user session
    """
    query = {"user_id": user.id}
    if session_id != 'all':
        query.update({"id": session_id})

    _ = await crud.session.update_many(query=query,
                                       values={"status": schemas.SessionStatus.LOGOUT})

    return TextResponse(message="OK")
