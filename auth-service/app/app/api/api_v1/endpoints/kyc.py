import secrets
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from app import schemas, crud
from app.api import deps
from app.core.verify import send_verification_message

router = APIRouter()


@router.post("/save/level1/")
async def save_kyc_leve_1(payload: schemas.KYCLevel1,
                          current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    await crud.user.update(current_user, {
        "first_name": payload.firstname,
        "last_name": payload.lastname,
        "middle_name": payload.middlename,
        "country.country_id": payload.countryid,
        "timezone.timezone_id": payload.timezoneid,
        "verification.verification_level": 1,
        "verification.verification_candidate": 2
    })
    return {
        "status": 'success',
        "message": 'User details for verification level 1 saved.',
        "verification": {
            "verification_level": 1,
            "verification_candidate": 2,
        }
    }


@router.post("/save/level2/")
async def save_kyc_leve_2(payload: schemas.KYCLevel2,
                          current_user: schemas.UserInDb = Depends(deps.get_current_user)) -> Any:
    await crud.user.update(current_user, {
        "city": payload.city,
        "phone": payload.phone,
        "postalcode": payload.postalcode,
        "state": payload.state,
        "street1": payload.street1,
        "street2": payload.street2
    })

    verify_token = secrets.token_hex(6)

    message_id = send_verification_message(payload.phone, verify_token)

    await crud.verify_request.create({
        "user_id": current_user.id,
        "phone": payload.phone,
        "token": verify_token,
        "message_id": message_id
    })

    return {
        "status": 'success',
        "message": 'Confirmation link sent to your phone',
        "verification": {
            "verification_level": 1,
            "verification_candidate": 2,
        }
    }


@router.get("/verify", response_class=HTMLResponse)
async def save_verify_phone(token: str) -> Any:
    request = await crud.verify_request.find_one({"token": token})

    if request:

        user = await crud.user.find_one({"id": request['user_id']})
        await crud.user.update(user, {
            "verification.verification_level": 2,
            "verification.verification_candidate": 3
        })

        message = "Your phone was confirmed"

    else:
        message = "Token invalid"

    return f"""
    <html>
        <head>
            <title>Phone verification</title>
        </head>
        <body>
            <h1>{message}</h1>
        </body>
    </html>
    """
