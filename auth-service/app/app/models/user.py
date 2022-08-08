from datetime import datetime
from typing import Optional

from api_contrib.models import description
from api_contrib.models.base import MongoDbModel
from pydantic import BaseModel, Field

from app.models.base import CommonConfig


class TimeZone(BaseModel):
    timezone: Optional[str] = 'Europe/Amsterdam'
    timezone_id: Optional[int] = 1


class Country(BaseModel):
    country_id: Optional[str] = ''
    country_name: Optional[str] = ''
    country_short: Optional[str] = ''


class Document(BaseModel):
    proof_of_identity: Optional[str] = ''
    proof_of_address: Optional[str] = ''


class Verification(BaseModel):
    verification_level: Optional[int] = 0
    verification_candidate: Optional[int] = 0


class User(MongoDbModel):
    username: str
    email: str
    password_hash: str
    account_type: Optional[str] = None
    mfa_enabled: bool = False
    mfa_secret: Optional[str] = None
    verified_email: bool = False
    pincode: Optional[str] = None
    account_locked: bool = False
    account_locked_reason: Optional[str] = None
    referred_by: Optional[str] = None
    is_active: bool = False
    is_admin: bool = False
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    phone: Optional[str]
    street1: Optional[str]
    street2: Optional[str]
    postal_code: Optional[str]
    state: Optional[str]
    city: Optional[str]
    ssnpassport: Optional[str]
    dayofbirth: Optional[str]
    documents: Optional[Document] = Document()
    verification: Optional[Verification] = Verification()
    country: Optional[Country] = Country()
    timezone: Optional[TimeZone] = TimeZone()

    class Config(CommonConfig):
        collection_name = "users"


class VerificationRequest(MongoDbModel):
    create_date: datetime = Field(default_factory=datetime.utcnow, description=description.CREATE_DATE)
    user_id: str
    phone: str
    token: str
    message_id: Optional[str]

    class Config(CommonConfig):
        collection_name = "verification_requests"
