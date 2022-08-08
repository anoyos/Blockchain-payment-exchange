from assertpy import assert_that

from tests.utils import super_user, auth_user
from tests.utils.admin_service_requests import add_market
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import MARKET_QUEUE

class TestGetMarketAll:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_tasknameis__get_assets(self):
        assert_that(False).is_true()