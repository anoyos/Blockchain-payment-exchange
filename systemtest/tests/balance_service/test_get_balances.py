from assertpy import assert_that
from requests import post

from tests.utils.a_transaction import aTransaction
from tests.utils import super_user
from tests.utils.auth_user import create_nonadmin_and_login, get_header_with_token
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BALANCE_QUEUE
from tests.utils.services import balances_url


class TestGetBalances:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_user_has_balance_when_get_balances_for_user_then_success(self):
        ### GIVEN
        auth_token = create_nonadmin_and_login("userGetWithdrawals")
        user_id = super_user.get_userid("userGetWithdrawals")
        headers = get_header_with_token(auth_token)

        celery = make_celery()
        deposit = aTransaction().with_transaction_type(1).with_amount(10).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_amount(-10).to_dict()
        transactions = [deposit, deposit_contra]
        celery_send(celery, user_id, transactions)

        ### WHEN
        response = post(balances_url, headers=headers)

        ### THEN
        assert_that(response.status_code).is_equal_to(200)

        payload = response.json()

        assert_that(payload.get('status')).is_equal_to('success')
        message = payload.get('message')
        assert_that(message).is_length(1)

        assert_that(message[0].get('asset_id')).is_equal_to(1)
        assert_that(message[0].get('balance')).is_type_of(int)
        assert_that(message[0].get('balance')).is_equal_to(10)

    def test_given_not_logged_in_when_asking_for_balances_then_fail(self):
        ### GIVEN

        ### WHEN
        response = post(balances_url)

        ### THEN
        payload = response.json()
        assert_that(payload.get('status')).is_equal_to('fail')
        assert_that(payload.get('message')).is_equal_to('ERR_INVALID_REQUEST')


def celery_send(celery, user_id, transactions):
    return celery.signature('balance.append', [user_id, transactions]) \
        .set(queue=BALANCE_QUEUE) \
        .set(expires=1) \
        .delay() \
        .get(1)