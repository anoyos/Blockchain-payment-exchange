from bullflag_commons.flask.bullflag_secure_resource import BullflagSecureAdminResource
from bullflag_commons.logging import get_logger
from bullflag_commons.rest_api import fail_response
from flask_restful import abort, reqparse


class AdminAddTrollboxRoomV1Resource(BullflagSecureAdminResource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.

    logger = get_logger(__name__)

    def __init__(self, **kwargs):
        self._trollbox_celery_producer = kwargs['trollbox_celery_producer']
        super(AdminAddTrollboxRoomV1Resource, self).__init__(kwargs['token_service'])

    def get(self):
        abort(403)

    def post(self):
        session_check = super().check_session()
        if not session_check.is_good:
            return session_check.rest_response
        try:
            parser = reqparse.RequestParser()
            parser.add_argument("name", type=str)
            args = parser.parse_args()
            room_name = args['name']
            if not room_name:
                return fail_response("ERR_NO_NAME_SUPPLIED")
            room_id = self._trollbox_celery_producer.add_room(room_name)
            self.logger.info(f"Added room with id {room_id}, name {room_name}")
            return {
                'status': 'success',
                'message': {
                    'id': room_id
                }
            }
        except Exception as e:
            self.logger.error(f"Failed adding market.", exc_info=e)
            return fail_response('ADD_MARKET_FAILED')
