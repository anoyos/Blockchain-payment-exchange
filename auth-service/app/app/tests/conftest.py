from typing import Generator

from fastapi.testclient import TestClient
from pytest import fixture

from app import schemas
from app.api import deps
from app.main import app


def patch_user():
    return schemas.UserInDb(**{'id': '60c2032f00294a8b9d9c59ec',
                               'username': 'razzor58',
                               'password_hash': 'a',
                               'mfa_enabled': False,
                               'verified_email': True,
                               'account_locked': False,
                               'is_active': False,
                               'is_admin': True,
                               'email': 'razzor58@gmail.com'})


@fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[deps.get_current_user] = patch_user
    with TestClient(app) as c:
        yield c
