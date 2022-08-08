from typing import Any, Dict

from fastapi import APIRouter, Depends, Path

from app import schemas, crud
from app.api import deps
import pytz
router = APIRouter()


@router.post("/full/",
             response_model=schemas.UserProfileResponse,
             response_model_exclude={"password_hash"})
async def get_full_profile(current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Get full the user's profile.
    """
    return {
        "message": current_user.dict(exclude={"password_hash"})
    }


@router.post("/set/timezone/{timezone_id}/")
async def set_user_timezone(timezone_id: int = Path(...),
                            current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    """
    Set user timezone
    """
    await crud.user.update(current_user, {
        "timezone.timezone": pytz.all_timezones[timezone_id],
        "timezone.timezone_id": timezone_id
    })
    return {
        "status": "success",
        "message": "OK"
    }


@router.post("/")
async def get_base_profile() -> Dict:
    return {
        "status": 'success',
        "message": 'User profile full',
        "user_profile_full": {
            "username": 'username',
            "email": 'email@address.com',
            "timezone": {
                "timezone": 'America/Cordoba',
                "timezone_id": 291,
            },
            "country": {
                "country_id": 43,
                "country_name": 'Chile',
                "country_short": 'CL',
            },
            "first_name": 'first-name',
            "last_name": 'last-name',
            "phone": '0123456789',
            "street1": 'Street & Number',
            "street2": None,
            "postal_code": '12345',
            "state": None,
            "city": 'City',
            "ssnpassport": 'passportnumber',
            "dayofbirth": None,
            "documents": {
                "proof_of_identity": None,
                "proof_of_address": None,
            },
            "verification": {
                "verification_level": 2,
                "verification_candidate": 3,
            },
            "referred_by": None,
            "account_locked": False,
            "verified_email": True,
            "mfa_enabled": True,
            "userid": '830f05ca-a677-41ec-832a-2bdf3c998a7f',
            "login_token": None,
            "account_locked_reason": None,
            "account_type": 'native',
            "id": 3,
            "is_admin": 1,
            "countryid": 43,
            "timezoneid": 291,
            "middle_name": None,
        }
    }


