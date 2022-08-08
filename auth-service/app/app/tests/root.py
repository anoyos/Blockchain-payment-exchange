from fastapi.testclient import TestClient

from app.core.config import settings


class TestAuth:

    # def test_login(self, client: TestClient) -> None:
    #     response = client.post(
    #         f"{settings.API_V1_STR}/login/",
    #         data={
    #             "username": "string",
    #             "password": "string"
    #         }
    #     )
    #     content = response.json()
    #     assert content['token'] != content['refresh_token']
    #     assert content["status"] == 'success'
    #
    # def test_refresh_token(self, client: TestClient) -> None:
    #     response = client.post(
    #         f"{settings.API_V1_STR}/refresh/",
    #         data={
    #             "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzMwODIzODYsInN1YiI6IjYwYzIwMzJmMDAyOTRhOGI5ZDljNTllYyJ9.Kd2DDtwuqHqyHU4I8vLZVfyzqs5xNNIdJvmDkmMnnZ4"
    #         }
    #     )
    #     content = response.json()
    #     assert content["status"] == 'success'

    def test_confirm_password_change(self, client: TestClient) -> None:
        response = client.get(
            f"{settings.API_V1_STR}/reset/password/verify",
            params={
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2MzMwODIzODYsInN1YiI6IjYwYzIwMzJmMDAyOTRhOGI5ZDljNTllYyJ9.Kd2DDtwuqHqyHU4I8vLZVfyzqs5xNNIdJvmDkmMnnZ4"
            }
        )
        code = response.status_code
        assert code == 200
