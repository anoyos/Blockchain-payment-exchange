from datetime import timedelta
from time import time
from typing import Any

import pycountry
import pytz
from api_contrib.schemas.base import TextResponse
from fastapi import APIRouter, Depends, HTTPException, Request

from fastapi.security import OAuth2PasswordRequestForm

from app import crud, schemas
from app.api import deps
from app.core import security
from app.core.config import settings

router = APIRouter()


async def create_new_session(user, request):
    user_agent = request.headers.get('user-agent')
    ip_address = request.headers.get('x-forwarded-for', 'unknown')

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    refresh_token = security.create_access_token(
        user.id, expires_delta=timedelta(
            minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES
        )
    )

    user_token = schemas.Token(
        auth_token=token,
        access_token=token,
        token=token,
        refresh_token=refresh_token,
        userid=user.id,
        expires_at=security.get_exp(token),
        servertime=int(time())
    )

    await crud.session.insert_one(schemas.UserSession(
        token=user_token.access_token,
        refresh_token=refresh_token,
        expires_at=user_token.expires_at,
        status=schemas.SessionStatus.ACTIVE,
        user_agent=user_agent,
        user_id=user.id,
        ip_address=ip_address
    ))
    return user_token


@router.post("/login/", response_model=schemas.Token)
async def login_access_token(request: Request,
                             form_data: OAuth2PasswordRequestForm = Depends()
                             ) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await create_new_session(user, request)


@router.post("/refresh/", response_model=schemas.Token)
async def refresh_user_session(request: Request,
                               payload: schemas.msg.RefreshToken
                               ) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """

    session = await crud.session.find_one(
        {"refresh_token": payload.refresh_token}
    )

    if not session:
        raise HTTPException(status_code=400, detail="Session not found")

    user = await crud.user.find_one({'id': session['user_id']})

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect refresh token")

    await crud.session.update(session, {"status": schemas.SessionStatus.LOGOUT})

    return await create_new_session(user, request)


@router.post("/tokenvalid/", response_model=schemas.UserInDb)
async def check_auth_token(current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Test access token
    """
    return current_user


# @router.post("/logout/", response_model=TextResponse)
# async def logout_current_session(user: schemas.UserInDb = Depends(deps.get_current_user),
#                                  token: str = Depends(deps.reusable_oauth2)
#                                  ) -> Any:
#     """
#     Close user session
#     """
#     session_filter = {
#         "user_id": user.id,
#         "token": token
#     }
#     _ = await crud.session.update_many(query=session_filter,
#                                        values={"status": schemas.SessionStatus.LOGOUT})
#     return {
#         "message": "OK"
#     }

@router.post("/logout/", response_model=TextResponse)
async def logout_current_session():
    return {
        "message": "OK"
    }


@router.post("/gettimezones/")
async def get_timezones() -> Any:
    """
    Gets a list of timezone arrays.
    """
    return {
        "status": "success",
        "message": [
            {"id": ind, "timezone": name} for ind, name in enumerate(pytz.all_timezones)
        ]
    }


@router.post("/getcountries/")
async def get_countries() -> Any:
    """
     list of country arrays.
    """
    return {
        "status": "success",
        "message": [
            {
                "country_code": country.alpha_2,
                "id": ind,
                "country_name": country.name,
            } for ind, country in enumerate(list(pycountry.countries))
        ]
    }


@router.post("/referralcode/")
async def get_referral_code(current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Gets the users unique referral code and the amount of referred users he/she has.
    """
    return {
        "status": "success",
        "message": {
            "referral_code": current_user.id,
            "referred_users": 0,
        },
    }
