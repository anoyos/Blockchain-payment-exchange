from typing import Any

from api_contrib.schemas.base import ResponseFormat
from fastapi import APIRouter, BackgroundTasks, HTTPException

from app import crud, schemas
from app.core.config import settings
from app.core.jwt import generate_confirm_token, verify_confirm_token
from app.utils import send_new_account_email

router = APIRouter()


@router.post("/register/", response_model=schemas.NewRecord)
async def create_user(
        *,
        user_in: schemas.UserCreate,
        background_tasks: BackgroundTasks
) -> Any:
    """
    Create new user.
    """
    user = await crud.user.get_by_email(email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await crud.user.create(user_in)
    if user_in.email:
        background_tasks.add_task(send_new_account_email,
                                  email_to=user_in.email,
                                  username=user_in.username,
                                  token=generate_confirm_token(settings, user_in.email))

    return schemas.NewRecord(message=schemas.IdResponse(id=user.id))


@router.post("/verify/", response_model=ResponseFormat)
async def signup_verify(
        *,
        token_in: schemas.ConfirmToken) -> Any:
    email = verify_confirm_token(settings, token_in.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_in_db = await crud.user.get_by_email(email=email)
    if not user_in_db:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system.",
        )

    await crud.user.update(user_in_db, {'verified_email': True})

    return ResponseFormat(message="Email verified  successfully")
