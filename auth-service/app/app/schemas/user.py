from typing import Optional

from api_contrib.schemas.base import ResponseFormat
from pydantic import EmailStr, BaseModel

from app.models.user import User


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    pincode: str
    referred_by: str


class UserUpdate(User):
    password: Optional[str] = None


class UserInDb(User):
    id: str


class UserProfile(UserInDb):
    password_hash: Optional[str] = None


class UserProfileResponse(ResponseFormat):
    message: UserProfile


class KYCLevel1(BaseModel):
    countryid: int
    firstname: str
    lastname: str
    middlename: str
    timezoneid: int


class KYCLevel2(BaseModel):
    city: str
    phone: str
    postalcode: str
    state: str
    street1: str
    street2: str
