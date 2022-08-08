from assertpy import assert_that
from requests import post

from tests.utils import super_user
from tests.utils import auth_user
from tests.utils.services import login_url

class TestLogin:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_existing_user_when_log_in_then_succeeds(self):
        # GIVEN
        body = auth_user.get_body("testuser", "testuser@mail.com")
        token = auth_user.register_user(body["username"], body["email"])
        auth_user.verify_registration(token)

        # WHEN
        response = post(login_url, body)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('success')
        assert_that(response.json().get('message')).is_equal_to("SUCC_LOGGED_IN")

    def test_given_existing_user_wrong_pwd_when_log_in_then_fails(self):
        # GIVEN
        body = auth_user.get_body("testuser", "testuser@mail.com")
        token = auth_user.register_user(body["username"], body["email"])
        auth_user.verify_registration(token)

        # WHEN
        body["password"] = "F4ulty123"
        body["password_repeat"] = "F4ulty123"
        response = post(login_url, body)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('errors')).is_equal_to(['Bad credentials'])
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")

    def test_given_non_existing_user_when_log_in_then_fails(self):
        # GIVEN
        body = auth_user.get_body("testuser", "testuser@mail.com")

        # WHEN
        response = post(login_url, body)

        # THEN
        # TODO: This test fails, if no service is running except for auth-service
        # test should fail based on that auth-service figures out bad-creds (seems like
        # bad-creds error is returned when celery task times out as well)
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('errors')).is_equal_to(['Bad credentials'])
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")
