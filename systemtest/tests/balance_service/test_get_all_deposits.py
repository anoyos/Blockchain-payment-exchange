from assertpy import assert_that
from requests import post

from tests.fixtures.balance_and_transactions import get_deposits_transactions
from tests.utils import super_user
from tests.utils.auth_user import create_nonadmin_and_login, get_header_with_token
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BALANCE_QUEUE
from tests.utils.services import all_deposits_url


class TestGetAllDeposits:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_user_has_deposits_when_get_all_deposits_for_user_then_success(self):
        ### GIVEN
        auth_token = create_nonadmin_and_login("userGetDeposits")
        user_id = super_user.get_userid("userGetDeposits")
        headers = get_header_with_token(auth_token)
        append_some_deposit(user_id)

        ### WHEN
        response = post(all_deposits_url, headers = headers)

        ### THEN
        assert_that(response.status_code).is_equal_to(200)

        payload = response.json()

        assert_that(payload.get('status')).is_equal_to('success')
        message = payload.get('message')
        assert_that(message).is_length(1)

        assert_that(message[0].get('asset_id')).is_equal_to(1)
        assert_that(message[0].get('timestamp_execution')).is_type_of(int)
        assert_that(message[0].get('amount')).is_equal_to(10.00000001)


def append_some_deposit(user_id):
    transactions = get_deposits_transactions(user_id)
    make_celery().signature('balance.append', [user_id, transactions]) \
        .set(queue=BALANCE_QUEUE) \
        .set(expires=1) \
        .delay() \
        .get(1)
