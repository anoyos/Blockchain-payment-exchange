from assertpy import assert_that
from requests import post

from tests.utils import super_user
from tests.utils.services import register_url, verify_registration_url, login_url

registration = {
    "password": "password123!",
    "password_repeat": "password123!",
    "pincode": "1234",
    "pincode_repeat": "1234"
}


def register_user(username, email):
    registration['username'] = username
    registration['email'] = email
    registration['email_repeat'] = email

    response = post(register_url, registration)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json().get('status')).is_equal_to('success')
    assert_that(response.json().get('message')).is_equal_to("SUCC_REGISTRATION_CHECK_MAIL")
    return response.json().get('__temp_token')


def verify_registration(temp_token):
    verification = {
        'token': temp_token
    }
    response = post(verify_registration_url, verification)
    assert_that(response.status_code).is_equal_to(200)
    assert_that(response.json().get('status')).is_equal_to('success')
    assert_that(response.json().get('message')).is_equal_to('SUCC_REGISTRATION_COMPLETE')


def login_user(email_or_username):
    login = {'password': 'password123!', 'mfatoken': "", 'username': email_or_username}
    response = post(login_url, login)
    assert_that(response.status_code).is_equal_to(200)
    return response.json().get('auth_token')


def create_nonadmin_and_login(username='testuser', email='testuser@mail.com') -> str:
    '''Creates user and returns token'''

    email = f"{email}"
    token = register_user(username, email)
    verify_registration(token)
    return login_user(username)


def create_admin_and_login(username, email="testadmin@mail.com") -> str:
    '''Creates admin user and returns token'''

    create_nonadmin_and_login(username, email)
    super_user.make_me_admin(username)
    return login_user(email)


def get_header_with_token(auth_token):
    return {
        "Authorization": "Bearer {}".format(auth_token)
    }


def get_body(username, email, password="password123!"):
    return {
        "username": username,
        "email": email,
        "email_repeat": email,
        "password": password,
        "password_repeat": password,
        "pincode": "1234",
        "pincode_repeat": "1234"
    }
