from typing import List
from typing import Optional

from api_contrib.schemas.base import ResponseFormat
from pydantic import BaseModel, Field, EmailStr

from app.models.keys import ApiKey


class NonAuthPasswordReset(BaseModel):
    email: EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class VerifyPasswordChange(BaseModel):
    token: str = Field(description="Verification token from email")
    password: str = Field(description="New user password")
    password_repeat: str = Field(description="New user password repeat")
    pincode: Optional[int] = Field(description="New user pin-code")
    mfatoken: Optional[str] = Field(description="If mfa enabled on account")


class OneStepPasswordChange(BaseModel):
    old_password: str = Field(description="Old user password")
    new_password: str = Field(description="New user password")
    new_password_repeat: str = Field(description="New user password repeat")


class VerifyPinCodeChange(BaseModel):
    token: str = Field(description="Verification token from email")
    password: str = Field(description="User password")
    pincode: int = Field(description="New user pin-code")
    pincode_repeat: int = Field(description="New user pin-code repeat")
    mfatoken: Optional[str] = Field(description="If mfa enabled on account")


class ActivateMfaRequest(BaseModel):
    mfatoken: str = Field(description="token given user on MFA site")
    password: str = Field(description="New user password")


class ApiKeyCreate(ApiKey):
    pass


class ApiKeyLegacy(ApiKey):
    added_ip: str = '172.16.201.1'
    apikeyid: Optional[str] = Field(description="Deprecated. Use `id` instead")
    created: int = 1624958992
    key: str = 'test_key'
    last_used: int = 1624958992
    last_used_from: str = '172.16.201.1'
    userid: Optional[str] = Field(description="Deprecated. Use `user_id` instead")
    set_cancelorder: bool = True
    set_createorder: bool = True
    set_deposit: bool = True
    set_enabled: bool = True
    set_trade: bool = True
    set_viewbalances: bool = True
    set_vieworders: bool = True
    set_withdrawal: bool = True

    def __init__(self, **data):
        super().__init__(**data)
        self.userid = self.user_id
        self.apikeyid = self.id


class ApiKeyResp(ResponseFormat):
    message: List[ApiKeyLegacy]
