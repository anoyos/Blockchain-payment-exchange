from typing import Generator
from unittest.mock import patch

from api_contrib.core.services import get_current_user
from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.core.constants import MOCK_BUY_ORDER, MOCK_SELL_ORDER, MOCK_MARKET, db_markets

from dotenv import load_dotenv
# from

def patch_user():
    return {'id': '', 'username': ''}


@fixture(scope="module")
def client() -> Generator:
    app.dependency_overrides[get_current_user] = patch_user
    with TestClient(app) as c:
        yield c


@fixture
def markets_list():
    return db_markets


@fixture
def market_filter():
    return {
        'symbol': 'XLTtBTC'
    }

@fixture
def market_filter_id():
    return {
        'marketid': MOCK_MARKET['id']
    }


@fixture
def buy_order():
    return MOCK_BUY_ORDER


@fixture
def sell_order():
    return MOCK_SELL_ORDER


@patch('app.market.connector.celery_app')
def get_celery_mock(mock_celery_app):
    return mock_celery_app


@fixture
def mock_user():
    """ Return values instead of Database calls """
    return {
        'username': 'test',
        'user_id': 'asda321e'
    }


@fixture
def mock_celery_app():
    """ Return values instead of Database calls """
    return get_celery_mock()
