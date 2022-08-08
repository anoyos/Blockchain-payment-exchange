from fastapi.testclient import TestClient
from pytest import mark

from app import crud
from app import schemas
from app.core.config import settings
from .conftest import patch_user


class TestUserSession:

    def setup(self):
        self.user = patch_user()
        mock_session = {
            'token': 'a',
            'expires_at': 1,
            'status': schemas.SessionStatus.ACTIVE,
            'user_agent': "apple mac (chrome)",
            'user_id': self.user.id,
            'ip_address': '0.0.0.0'
        }
        for i in range(2):
            self.session_id = crud.session.create_sync(mock_session)

    def test_get_user_session(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/session/list/"
        )
        content = response.json()
        assert content["status"] == 'success'

    @mark.parametrize("logout_all", [True, False])
    def test_logout_all(self, logout_all, client: TestClient) -> None:
        s_id = 'all' if logout_all else self.session_id
        response = client.post(
            f"{settings.API_V1_STR}/session/logout/{s_id}/"
        )
        content = response.json()
        assert content["status"] == 'success'
