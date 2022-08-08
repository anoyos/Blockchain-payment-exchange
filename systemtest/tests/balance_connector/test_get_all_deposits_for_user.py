import time
from typing import List
from uuid import uuid4

from assertpy import assert_that

from tests.utils.a_transaction import aTransaction
from tests.utils import super_user
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BALANCE_QUEUE
from tests.utils.system import SYSTEM_UUID


class TestGetAllDepositsForUser:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_get_all_deposits_for_user_with_user_id_as_arg(self):
        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_amount(10).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_amount(-10).to_dict()
        transactions = [deposit, deposit_contra]

        celery.signature('balance.append', [user_id, transactions]) \
            .set(queue=BALANCE_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # WHEN
        result = celery.signature('balance.get_all_deposits_for_user', [user_id]) \
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
