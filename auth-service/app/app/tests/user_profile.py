from fastapi.testclient import TestClient

from app.core.config import settings


class TestUserProfile:

    # def test_get_profile(self, client: TestClient) -> None:
    #     response = client.post(
    #         f"{settings.API_V1_STR}/profile/full/"
    #     )
    #     content = response.json()
    #     assert content["status"] == 'success'
    #
    # def test_update_profile(self, client: TestClient) -> None:
    #     response = client.post(
    #         f"{settings.API_V1_STR}/profile/save/level1/",
    #         json={
    #             "countryid": 1,
    #             "firstname": "test",
    #             "lastname": "test",
    #             "middlename": "test",
    #             "timezoneid": 1
    #         }
    #     )
    #     content = response.json()
    #     assert content["status"] == 'success'
    #
    # def test_update_profile_2(self, client: TestClient) -> None:
    #     response = client.post(
    #         f"{settings.API_V1_STR}/profile/save/level2/",
    #         json={
    #             "city": "Novosibirsk",
    #             "phone": '+79139861302',
    #             "postalcode": 630099,
    #             "state": "NSO",
    #             "street1": "krasny",
    #             "street2": "-"
    #         }
    #     )
    #     content = response.json()
    #     assert content["status"] == 'success'

    def test_set_timezone(self, client: TestClient) -> None:
        response = client.post(
            f"{settings.API_V1_STR}/profile/set/timezone/2/",
            json={
            }
        )
        content = response.json()
        assert content["status"] == 'success'