from fastapi.testclient import TestClient

from app.core.config import settings


class TestAdminUsers:

    def test_get_all_users(self, client: TestClient) -> None:
        response = client.post(
             f"{settings.API_V1_STR}/admin/list"
        )
        content = response.json()
        assert content["status"] == 'success'

    def test_user_count(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/admin/count"
        )
        content = response.json()
        assert content["status"] == 'success'
