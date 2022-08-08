from uuid import uuid4

from assertpy import assert_that, fail

from tests.utils import super_user
from tests.utils.a_transaction import aTransaction
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BALANCE_QUEUE


class TestAppend:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_new_transaction_when_append_then_success(self):
        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_amount(10.5).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_amount(-10.5).to_dict()
        transactions = [deposit, deposit_contra]

        # WHEN
        result = celery_send(celery, user_id, transactions)
        transactions = super_user.get_transactions_from_db()
        transaction_ids = [str(transaction['transaction_id']) for transaction in transactions]

        # THEN
        assert_that(result).is_equal_to(transaction_ids)

    def test_given_duplicate_transaction_sent_when_append_then_it_is_not_saved(self):

        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_amount(10.5).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_amount(-10.5).to_dict()
        transactions = [deposit, deposit_contra]

        result_1 = celery_send(celery, user_id, transactions)
        transactions_after_1 = super_user.get_transactions_from_db()
        transaction_ids_after_1 = [str(transaction['transaction_id']) for transaction in transactions_after_1]

        # WHEN

        # Send the same transaction again
        result_2 = celery_send(celery, user_id, transactions)

        transactions_after_2 = super_user.get_transactions_from_db()
        transaction_ids_after_2 = [str(transaction['transaction_id']) for transaction in transactions_after_2]

        # THEN
        assert_that(len(result_1)).is_equal_to(2)
        # No result should be returned this time
        assert_that(len(result_2)).is_equal_to(0)

        assert_that(result_1).is_equal_to(transaction_ids_after_1)

        expected_new_transaction_id_after_second_append = list(
            set(transaction_ids_after_2) - set(transaction_ids_after_1))
        assert_that(result_2).is_equal_to(expected_new_transaction_id_after_second_append)

    def test_given_transaction_have_bad_number_of_decimals_when_append_then_fails(self):

        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        # should be max 8 decimals
        deposit = aTransaction().with_transaction_type(1).with_amount(0.000000001).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_amount(-0.000000001).to_dict()
        bad_trans = [deposit, deposit_contra]

        # WHEN
        try:
            celery_send(celery, user_id, bad_trans)
            fail("should have raised error")
        except Exception as e:
            # THEN

            transactions = super_user.get_transactions_from_db()
            assert_that(transactions).is_length(0)
            assert_that(str(e)).contains("Max 8 decimals allowed. Transactions: ")

    def test_given_transactions_not_break_even_when_append_then_fails(self):

        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_amount(1).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_amount(-1.1).to_dict()
        bad_trans = [deposit, deposit_contra]

        # WHEN
        try:
            celery_send(celery, user_id, bad_trans)
            fail("should have raised error")
        except Exception as e:
            # THEN

            transactions = super_user.get_transactions_from_db()
            assert_that(transactions).is_length(0)
            assert_that(str(e)).contains("Sums of transactions does not break even. Transactions: ")

    def test_given_two_transactions_having_different_execution_times_when_append_then_fails(self):

        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_ts_exec(1000).with_amount(1).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1000).with_ts_exec(1001).with_amount(-1).to_dict()
        bad_trans = [deposit, deposit_contra]

        # WHEN
        try:
            celery_send(celery, user_id, bad_trans)
            fail("should have raised error")
        except Exception as e:
            # THEN

            transactions = super_user.get_transactions_from_db()
            assert_that(transactions).is_length(0)
            assert_that(str(e)).contains("Execution timestamps do not match. Transactions: ")

    def test_given_transaction_is_deposit_when_offset_account_is_not_debited_then_fails(self):

        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_amount(1).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1).with_amount(-1).to_dict()
        bad_trans = [deposit, deposit_contra]

        # WHEN
        try:
            celery_send(celery, user_id, bad_trans)
            fail("should have raised error")
        except Exception as e:
            # THEN

            transactions = super_user.get_transactions_from_db()
            assert_that(transactions).is_length(0)
            assert_that(str(e)).contains("Missing sys account transaction. Transactions: ")

    # TODO await transaction_type: transaction fee to make withdrawal transaction proper (in fixture.py)
    def test_given_transaction_is_withdrawal_when_offset_account_is_not_credited_then_fails(self):

        # GIVEN
        celery = make_celery()
        user_id = uuid4()
        deposit = aTransaction().with_transaction_type(1).with_amount(1).to_dict()
        deposit_contra = aTransaction().with_transaction_type(1).with_amount(-1).to_dict()
        bad_trans = [deposit, deposit_contra]

        # WHEN
        try:
            res = celery_send(celery, user_id, bad_trans)
            raise Exception('Should not fail')
        except:
            pass
        transactions = super_user.get_transactions_from_db()

        # THEN
        assert_that(transactions).is_length(0)

    # TODO await transaction_type: transaction fee
    def given_transaction_is_withdrawal_when_fee_transaction_is_missing_then_fails(self):
        # trans 1 -> withdrawal
        # trans 2 -> contra account trans
        # no trans 3 -> there should be a fee trans, appending to SYSTEM_ACCOUNT
        assert_that(False).is_true()


def celery_send(celery, user_id, transactions):
    return celery.signature('balance.append', [user_id, transactions]) \
        .set(queue=BALANCE_QUEUE) \
        .set(expires=1) \
        .delay() \
        .get(1)
