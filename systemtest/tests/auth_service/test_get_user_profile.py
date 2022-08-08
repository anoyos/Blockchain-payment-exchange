from assertpy import assert_that
from requests import post

from tests.utils import super_user, auth_user
from tests.utils.auth_user import get_header_with_token
from tests.utils.services import get_profile


class TestGetUserProfile:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_logged_in_profile_is_there(self):
        # 1. URL är /api/v1/user/profile/
        # 2. Tror vi ska lägga till ett clean-db-steg för nya tabeller (Countries, User_details) i super_user
        assert_that(False).is_true()

    def test_given_not_logged_in_response_X_is_returned(self):
        assert_that(False).is_true()

    def test_remove_later(self):
        token = auth_user.create_nonadmin_and_login("testuser", "testuser@mail.com")
        headers = get_header_with_token(token)
        response = post(get_profile, headers=headers)
        assert_that(response.json().get('status')).is_equal_to('success')