from assertpy import assert_that

from tests.utils import super_user


class TestSignup:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_signup_task(self):
        assert_that(False).is_true()
