from assertpy import assert_that

from tests.utils import super_user
from tests.utils.auth_user import create_nonadmin_and_login
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import WALLET_QUEUE
from tests.utils.wallet_service_requests.requests import get_deposit_address


class TestFreeDepositAddressCount:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_free_deposit_address_count(self):
        # GIVEN
        auth_token = create_nonadmin_and_login("testfreedepositcount")
        get_deposit_address(1, auth_token)
        celery = make_celery()

        # WHEN
        result = celery.signature("wallet.free_deposit_address_count", [1])\
            .set(queue=WALLET_QUEUE)\
            .set(expires=1)\
            .delay()\
            .get(1)

        # THEN
        assert_that(result).is_equal_to(50)
