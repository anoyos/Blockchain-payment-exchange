from api_contrib.schemas.base import ResponseStatus
from fastapi.testclient import TestClient

from app.core.config import settings



class TestProfileRoute:
    def test_get_usd_value(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/profile/usdvalue/"
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS
