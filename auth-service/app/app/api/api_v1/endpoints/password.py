from typing import Any

from api_contrib.schemas.base import TextResponse
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse
from app.core.security import verify_password, get_password_hash

from app import schemas
from app import crud
from app.api import deps
from app.core.config import settings
from app.core.jwt import generate_confirm_token, verify_confirm_token
from app.utils import send_reset_password_email

router = APIRouter()


@router.post("/password/request/",
             response_model=TextResponse)
async def request_password_change(
        payload: schemas.NonAuthPasswordReset,
        background_tasks: BackgroundTasks) -> Any:
    """
    Change password step 1: Request
    """
    user = await crud.user.find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")

    if payload.email:
        background_tasks.add_task(send_reset_password_email,
                                  email_to=payload.email,
                                  token=generate_confirm_token(settings, payload.email))
    return TextResponse(message="Check email for instructions")


@router.post("/password/verify/")
async def request_password_change(payload: schemas.VerifyPasswordChange) -> Any:
    """
    Change password step 2: Verify
    """
    if payload.password != payload.password_repeat:
        raise HTTPException(status_code=400, detail="New passwords mismatch")

    user_email = verify_confirm_token(settings, payload.token)
    user = await crud.user.find_one({"email": user_email})
    await crud.user.update(user, {"password_hash": get_password_hash(password=payload.password)})
    return {
        "status": "success",
        "message": "Password successfully changed"
    }


@router.post("/password/auth_request/",
             response_model=TextResponse)
async def change_password_from_user(
        payload: schemas.OneStepPasswordChange,
        background_tasks: BackgroundTasks,
        user_in: schemas.UserInDb = Depends(deps.get_current_user),
        ) -> Any:
    """
    Change password by logged-in user
    """
    if payload.new_password != payload.new_password_repeat:
        raise HTTPException(status_code=400, detail="New passwords mismatch")

    if not verify_password(plain_password=payload.old_password, hashed_password=user_in.password_hash):
        raise HTTPException(status_code=400, detail="Old password incorrect password")

    await crud.user.update(user_in, {"password_hash": get_password_hash(password=payload.new_password)})

    if user_in.email:
        background_tasks.add_task(send_reset_password_email,
                                  email_to=user_in.email,
                                  username=user_in.username)
    return TextResponse(message="Password successfully changed")


@router.post("/pincode/request/", response_model=TextResponse)
async def request_password_change(current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Change pin_code step 1: Request
    """
    return TextResponse(message="Check email for instructions")


@router.post("/pincode/verify/", response_model=TextResponse)
async def request_password_change(payload: schemas.VerifyPinCodeChange) -> Any:
    """
    Change pin_code step 2: Verify
    """
    return TextResponse(message="Pin-code successfully updated")
