from assertpy import assert_that
from requests import post, get

from tests.utils import super_user
from tests.utils.auth_user import create_admin_and_login, get_header_with_token, create_nonadmin_and_login
from tests.utils.services import add_trollbox_room, trollbox_rooms


class TestGetAllRooms:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_get_rooms(self):
        ### GIVEN
        admin_token = create_admin_and_login("adminuser")
        headers = get_header_with_token(admin_token)
        payload = {'name': 'the_backyard'}
        response = post(add_trollbox_room, data=payload, headers=headers)
        assert_that(response.json()['status']).is_equal_to('success')

        non_admin_token = create_nonadmin_and_login("trollboxuser", "trollbox_user@mail.com")
        non_admin_headers = get_header_with_token(non_admin_token)

        ### WHEN
        response = get(trollbox_rooms, headers=non_admin_headers)

        ### THEN
        payload = response.json()
        assert_that(response.status_code).is_equal_to(200)
        assert_that(payload['status']).is_equal_to('success')
        rooms = payload['message']
        assert_that(rooms).is_length(1)
        assert_that(rooms[0]['id']).is_length(36)
        assert_that(rooms[0]['name']).is_equal_to("the_backyard")
