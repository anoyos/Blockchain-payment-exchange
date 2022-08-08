from assertpy import assert_that

from tests.utils import super_user


class TestGetAllRooms:

    @classmethod
    def setup_class(cls):
        pass

    def setup_method(self, method):
        super_user.delete_all()

    def test_send_messages(self):
        ### GIVEN

        # create admin and add a room
        # create a non-admin, log in, get a room ID, post a message /api/v1/trollbox/rooms/<room_id>/message
        # check history, that message is there POST /api/v1/trollbox/rooms/<room_id>
        assert_that(False).is_true()

    def test_delete_messages(self):
        ### GIVEN

        # create admin and add a room
        # create a non-admin, log in, get a room ID, post a message /api/v1/trollbox/rooms/<room_id>/message
        # check history, that message is there POST /api/v1/trollbox/rooms/<room_id>
        # DELETE message
        # check history that it is gone
        assert_that(False).is_true()

    def test_get_history(self):
        # insert some messages (2)
        # query for history of room X
        # assert messages, and order of them(!)

        assert_that(False).is_true()
