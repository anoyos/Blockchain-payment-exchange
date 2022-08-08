from assertpy import assert_that

from tests.utils import super_user
from tests.utils.auth_user import create_admin_and_login, create_nonadmin_and_login


class TestAddTrollboxRoom:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_admin_when_adding_trollboxroom_then_works(self):
        # GIVEN
        token = create_admin_and_login("adminuser")
        "post a new trollbox room"
        "see that ok back"
        assert_that(False).is_true()

    def test_given_nonadmin_when_adding_trollboxroom_then_works(self):
        # GIVEN
        token = create_nonadmin_and_login("adminuser")
        "post a new trollbox room"
        "see that fail back"
        assert_that(False).is_true()
