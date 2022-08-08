from fastapi.testclient import TestClient

from app.core.config import settings


class TestApiKey:

    def test_create_api_key(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/apikey/create/"
        )
        content = response.json()
        assert content["status"] == 'success'

    def test_api_key_list(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/apikey/"
        )
        content = response.json()
        assert content["status"] == 'success'
