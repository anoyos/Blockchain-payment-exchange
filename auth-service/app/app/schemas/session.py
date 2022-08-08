from typing import List, Optional
from user_agents import parse
from api_contrib.schemas.base import ResponseFormat

from app.models.session import Session


class UserSession(Session):
    pass


class SessionStatus:
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    LOGOUT = "LOGOUT"


class SessionObject(Session):
    sessionid: Optional[str]

    def __init__(self, **data):
        super().__init__(**data)
        self.sessionid = self.id
        ua = parse(self.user_agent)
        self.user_agent = f'{ua.device.brand} {ua.device.model} ({ua.browser.family})'


class SessionListResponse(ResponseFormat):
    message: List[SessionObject]
