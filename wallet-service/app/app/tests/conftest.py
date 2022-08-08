from typing import Generator

from api_contrib.core.services import get_current_user
from fastapi.testclient import TestClient
from pytest import fixture

from app import crud
from app.db.init_db import prepare_database
from app.main import app

USER = {'id': '6059ca50b695b1142c11c7bm'}
USER_2 = {'id': '61095d1d514535be25a449d7'}


@fixture
def eth_deposit_address():
    return '0xcAd3B024F57e9595B7Bed1b33C7AECD35D74fe0e'

@fixture
def mock_user():
    return USER


def patch_user():
    return USER


@fixture(scope="session", autouse=True)
def client() -> Generator:
    app.dependency_overrides[get_current_user] = patch_user
    with TestClient(app) as c:
        yield c


def remove_deposit_request():
    crud.deposit_request = crud.deposit_addresses.delete_many_sync({
        'user_id': USER_2['id']
    })


@fixture(scope='session', autouse=True)
def setup():
    # create BTC, DOGE, LTC, DASH wallets if not exists
    prepare_database()
    # Remove deposit addresses for second users to cover `create new address` cases
    remove_deposit_request()
    yield
