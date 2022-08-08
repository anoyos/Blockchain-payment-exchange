# TODO error if token not successfully revoked

from assertpy import assert_that
from requests import post

from tests.utils import super_user
from tests.utils import auth_user
from tests.utils.services import logout_url


class TestLogout:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_logged_in_user_when_logout_then_success(self):
        # GIVEN
        body = auth_user.get_body("testuser", "testuser@mail.com")
        auth_user.create_nonadmin_and_login(body["username"], body["email"])

        # WHEN
        response = post(logout_url, body)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('success')
        assert_that(response.json().get('message')).is_equal_to("SUCC_LOGGED_OUT")
