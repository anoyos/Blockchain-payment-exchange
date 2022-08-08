from api_contrib.crud.base_mongo import CRUDBaseMongo

from app.models.keys import ApiKey
from app.models.session import Session
from app.models.user import User, VerificationRequest

from .session import CRUDSession
from .user import CRUDUser

user = CRUDUser(User)
session = CRUDSession(Session)
api_key = CRUDBaseMongo(ApiKey)
verify_request = CRUDBaseMongo(VerificationRequest)
