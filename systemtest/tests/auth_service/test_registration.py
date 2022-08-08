# TODO register, register again - then verify should succeed!

from assertpy import assert_that
from requests import post

from tests.utils import super_user, auth_user
from tests.utils.services import register_url


class TestRegistration:

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_new_user_when_register_then_success(self):
        # GIVEN
        body = auth_user.get_body('testuser', 'testuser@mail.com')

        # WHEN
        response = post(register_url, body)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('success')
        assert_that(response.json().get('message')).is_equal_to("SUCC_REGISTRATION_CHECK_MAIL")
        assert_that(response.json().get('__temp_token')).is_not_empty()

    def test_given_existing_username_when_register_then_fails(self):
        # GIVEN
        username = 'testuser'
        email = 'testuser@mail.com'
        auth_user.create_nonadmin_and_login(username, email)
        header = auth_user.get_body(username, 'other@mail.com')

        # WHEN
        response = post(register_url, header)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('errors')).is_equal_to('Username or email address is already taken')
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")

    def test_given_existing_email_when_register_then_fails(self):
        # GIVEN
        username = 'testuser'
        email = 'testuser@mail.com'
        auth_user.create_nonadmin_and_login(username, email)
        header = auth_user.get_body('other', email)

        # WHEN
        response = post(register_url, header)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('errors')).is_equal_to('Username or email address is already taken')
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")

    def test_given_pending_user_verification_when_register_with_same_username_different_email_then_fails(self):
        # GIVEN
        username = 'testuser'
        email = 'testuser@mail.com'
        auth_user.register_user(username, email)
        header = auth_user.get_body(username, 'other@mail.com')

        # WHEN
        response = post(register_url, header)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('errors')).is_equal_to('Username or email address is already taken')
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")

    def test_given_pending_user_verification_when_register_with_same_email_different_username_then_fails(self):
        # GIVEN
        username = 'testuser'
        email = 'testuser@mail.com'
        auth_user.register_user(username, email)
        header = auth_user.get_body('other', email)

        # WHEN
        response = post(register_url, header)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('errors')).is_equal_to('Username or email address is already taken')
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")

    def test_given_pending_user_verification_when_register_with_same_email_same_username_then_success(self):
        # TODO complete email connector
        # GIVEN
        username = 'testuser'
        email = 'testuser@mail.com'
        auth_user.register_user(username, email)
        body = auth_user.get_body(username, email)

        # WHEN
        response = post(register_url, body)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('success')
        assert_that(response.json().get('message')).is_equal_to("SUCC_REGISTRATION_CHECK_MAIL")
        assert_that(response.json().get('__temp_token')).is_not_empty()

    def test_given_bad_password_then_fails(self):
        # GIVEN
        header = auth_user.get_body('testuser', 'testuser@mail.com', 'bad')

        # WHEN
        response = post(register_url, header)

        # THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json().get('status')).is_equal_to('fail')
        assert_that(response.json().get('message')).is_equal_to("ERR_VALIDATION_ERROR")
        assert_that(response.json().get('__temp_token')).is_none()

    def test_given_registration_twice_with_same_user_and_email_when_using_second_reg_token_to_verify_then_success(self):
        # 1. register - success
        # 2. register same everything, again - success
        # 3. pass second-attempt registration token, to verify endpoint - success
        # 4. login - successx
        assert_that(False).is_true()

    def test_given_referral_code_issued_when_user_register_with_it_then_it_works(self):
        # 1. pass a referral code on registration form
        # 2. complete registration, verification and login
        # 3. Verify in database that referral-user is referred on registered user.
        assert_that(False).is_true()
