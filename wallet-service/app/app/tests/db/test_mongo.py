from api_contrib.schemas.base import ResponseStatus

from app.core.config import settings


class TestCrud:
    def test_db_query(self, client):
        # data = crud.last_prices.find_one_sync({})
        # assert 'tBTC' in data['prices']
        response = client.post(
            f"{settings.API_V1_STR}/profile/usdvalue/"
        )
        content = response.json()
        assert content["status"] == ResponseStatus.SUCCESS
