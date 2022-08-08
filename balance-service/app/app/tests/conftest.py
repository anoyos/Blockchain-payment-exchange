from typing import Generator


from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app


def patch_user():
    return {'id': '61b8cd9a67fbc8324e7272ec', 'username': 'razzor58@gmail.com'}


@fixture(scope="module")
def client() -> Generator:
    from api_contrib.core.services import get_current_user
    app.dependency_overrides[get_current_user] = patch_user
    with TestClient(app) as c:
        yield c
