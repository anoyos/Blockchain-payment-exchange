import socketio
from assertpy import assert_that
from requests import post, get, delete

from tests.utils import super_user
from tests.utils.async_assert_that import async_assert_that
from tests.utils.auth_user import get_header_with_token, create_nonadmin_and_login, create_admin_and_login
from tests.utils.services import new_trollbox_message, trollbox_rooms, add_trollbox_room, delete_trollbox_message
from tests.utils.websockets.trollbox_store import TrollboxStore


class TestTrollboxRoom:
    sio = socketio.Client(logger=True, engineio_logger=True)

    @classmethod
    def setup_class(cls):
        print("before class-setups")

    def setup_method(self, method):
        super_user.delete_all()

    def teardown_method(self, method):
        self.sio.disconnect()

    def test_given_new_trollbox_message_when_websocket_connected_then_new_event_is_received(self):
        ### GIVEN
        store = TrollboxStore("/")
        connect_socket(self.sio, store)

        auth_token = create_nonadmin_and_login("trollboxChatGuy")
        headers = get_header_with_token(auth_token)

        room_id = get_room_id()
        payload = {"msg": "Hi from systemtest"}

        ### WHEN
        post(new_trollbox_message(room_id), payload, headers=headers)

        ### THEN
        async_assert_that(store.new_messages).is_length(1)
        async_assert_that(store.new_messages[0]['data']['message']).is_equal_to("Hi from systemtest")
        async_assert_that(store.new_messages[0]['data']['room_id']).is_equal_to(room_id)

    def test_given_delete_trollbox_message_when_websocket_connected_then_delete_event_is_received(self):
        ### GIVEN
        store = TrollboxStore("/")
        connect_socket(self.sio, store)

        auth_token = create_nonadmin_and_login("trollboxChatGuy")
        headers = get_header_with_token(auth_token)

        room_id = get_room_id()
        payload = {"msg": "Hi from systemtest"}
        post(new_trollbox_message(room_id), payload, headers=headers)
        async_assert_that(store.new_messages).is_length(1)
        message_id = store.new_messages[0]['data']['id']
        ### WHEN

        response = delete(delete_trollbox_message(room_id, message_id), headers=headers)

        ### THEN
        assert_that(response.status_code).is_equal_to(200)
        assert_that(response.json()['message']).is_equal_to("SUCC_MSG_DELETED")
        async_assert_that(store.deleted_messages).is_length(1)
        assert_that(store.deleted_messages[0]['data']['id']).is_equal_to(message_id)
        assert_that(store.deleted_messages[0]['data']['room_id']).is_equal_to(room_id)


def connect_socket(sio, store):
    sio.register_namespace(store)
    sio.connect("ws://localhost:5001", transports=['websocket'])


def get_room_id():
    admin_auth_token = create_admin_and_login("trollboxAdmin")
    admin_headers = get_header_with_token(admin_auth_token)
    post(add_trollbox_room, data={'name': 'trollbox'}, headers=admin_headers)

    rooms_response = get(trollbox_rooms, headers=admin_headers)
    return rooms_response.json()['message'][0]['id']
