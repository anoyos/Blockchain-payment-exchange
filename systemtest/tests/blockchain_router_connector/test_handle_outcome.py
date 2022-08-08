from uuid import uuid4

from assertpy import assert_that

from tests.utils import super_user
from tests.utils.celery import make_celery
from tests.utils.queue_definitions import BALANCE_QUEUE, BLOCK_CHAIN_ROUTER_QUEUE


class TestHandleOutcome:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_handle_outcome(self):
        # GIVEN
        celery = make_celery()

        # WHEN
        result = celery.signature('blockchain_router.handle_outcome', ["some outcome - just echoed at the moment"]) \
            .set(queue=BLOCK_CHAIN_ROUTER_QUEUE) \
            .set(expires=1) \
            .delay() \
            .get(1)

        # THEN
        assert_that(result).is_equal_to("some outcome - just echoed at the moment")
