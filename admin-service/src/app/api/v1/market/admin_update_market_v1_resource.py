from bullflag_commons.flask.bullflag_secure_resource import BullflagSecureAdminResource
from bullflag_commons.logging import get_logger
from flask_restful import reqparse, abort

from app.api.util import cast_value
from app.api.v1.market.valid_market_settings import valid_settings


class AdminUpdateMarketV1Resource(BullflagSecureAdminResource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.

    logger = get_logger(__name__)

    def __init__(self, **kwargs):
        self._market_service = kwargs['market_service']
        super(AdminUpdateMarketV1Resource, self).__init__(kwargs['token_service'])

    def get(self):
        abort(403)

    def post(self):
        session_check = super(AdminUpdateMarketV1Resource, self).check_session()
        if not session_check.is_good:
            return session_check.rest_response

        parser = reqparse.RequestParser()
        parser.add_argument("market_id", type=str)
        parser.add_argument("setting", type=str)
        parser.add_argument("value")
        args = parser.parse_args()

        market_id = args.get('market_id')
        setting = args.get('setting')
        value = cast_value(args.get('value'))

        if not self._valid_setting_found(setting, value):
            self.logger.error("No valid setting submitted. {}".format(args))
            return {"status": "fail", "message": "ERR_INVALID_SETTING"}, 200

        setting_payload = {
            'market_id': market_id,
            'setting': args.get('setting'),
            'value': value,
        }
        try:
            self._market_service.update_market_setting(setting_payload)
        except Exception as exec:
            self.logger.error("Failed to update market setting", exc_info=exec)
            return {"status": "fail", "message": "ERR_FAILED_TO_SET"}, 200

        return {"status": "success", "message": "SUCC_UPDATED"}, 200

    @staticmethod
    def _valid_setting_found(setting, value):
        if type(setting) is not str or setting == None or value == None:
            return False
        valids = [_is_valid(entry, setting, value) for entry in valid_settings]
        return True in valids


def _is_valid(valid_setting_type, setting, value) -> bool:
    for valid_setting, valid_type in valid_setting_type.items():
        if valid_setting == setting and valid_type == type(value):
            return True
    return False
