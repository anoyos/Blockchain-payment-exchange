from assertpy import assert_that
from requests import post

from tests.utils import super_user
from tests.utils.auth_user import create_nonadmin_and_login, get_header_with_token
from tests.utils.services import referral_codes_url


class TestReferralCode:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_given_user_when_get_referral_code_then_works(self):
        ### GIVEN
        token = create_nonadmin_and_login("refCodeUser")
        headers = get_header_with_token(token)

        ### WHEN
        response = post(referral_codes_url, headers=headers)

        ### THEN
        payload = response.json()

        assert_that(payload['status']).is_equal_to('success')
        assert_that(payload['message']['referral_code']).is_length(36)
        assert_that(payload['message']['referred_users']).is_equal_to(0)
