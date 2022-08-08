from api_contrib.schemas.base import ResponseStatus
from fastapi.testclient import TestClient

from app.core.config import settings


class TestFavoritesRoute:

    def test_add_asset_to_favorites(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/wallet/favorite/61ac9609-1ddd-4890-bfde-ac2929b7344f/add/"
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS

    def test_get_favorites(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/wallet/favorite/get/"
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS
