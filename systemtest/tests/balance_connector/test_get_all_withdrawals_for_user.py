from uuid import uuid4

from assertpy import assert_that

from tests.utils import super_user
from tests.utils.a_transaction import aTransaction
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BALANCE_QUEUE


class TestGetAllWithdrawalsForUser:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_get_all_withdrawals_for_user_with_user_id_as_arg(self):
        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        withdrawal = aTransaction().with_transaction_type(2).with_amount(10).with_metadata( \
            {'txid': 'abc123', 'to_address': 'xxx111', 'from_address': 'xxx111'}).to_dict()
        withdrawal_contra = aTransaction().with_transaction_type(1000).with_amount(-10).to_dict()
        transactions = [withdrawal, withdrawal_contra]
        celery.signature('balance.append', [user_id, transactions]) \
            .set(queue=BALANCE_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # WHEN
        result = celery.signature('balance.get_all_withdrawals_for_user', [user_id]) \
            .set(queue=BALANCE_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(len(result)).is_equal_to(1)

        assert_that(result[0]['id']).is_type_of(str)
        assert_that(len(result[0]['id'])).is_equal_to(36)
        assert_that(result[0]['asset_id']).is_equal_to(1)
        assert_that(result[0]['amount']).is_equal_to(10)
