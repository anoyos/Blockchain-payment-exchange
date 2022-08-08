from bullflag_commons.crypto import TokenService
from bullflag_commons.exception import BullflagException
from bullflag_commons.flask.bullflag_secure_resource import BullflagSecureAdminResource
from bullflag_commons.logging import get_logger
from flask_restful import reqparse, abort

from app.service.market_service import MarketService


class AdminAddMarketV1Resource(BullflagSecureAdminResource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.

    logger = get_logger(__name__)

    def __init__(self, **kwargs):
        self._market_service = kwargs['market_service']
        super(AdminAddMarketV1Resource, self).__init__(kwargs['token_service'])

    def get(self):
        abort(403)

    def post(self):
        session_check = super().check_session()
        if not session_check.is_good:
            return session_check.rest_response

        parser = reqparse.RequestParser()
        parser.add_argument("asset_id", type=int)
        parser.add_argument("base_asset_id", type=int)
        args = parser.parse_args()

        try:
            asset_id = args['asset_id']
            base_asset_id = args['base_asset_id']
        except Exception as exec:
            self.logger.error("Creating market threw exception", exc_info=exec)
            return {"status": "fail", "message": "ERR_INVALID_CURRENCYIDS"}, 200

        try:
            market_id = self._market_service.create_market(base_asset_id, asset_id)
        except BullflagException as bf_exec:
            self.logger.error("Creating market threw exception. {}".format(bf_exec.message), exc_info=bf_exec)
            return {'status': 'fail', 'message': bf_exec.message}, 200
        except Exception as exec:
            self.logger.error("Creating market threw exception", exc_info=exec)
            if exec.args[0] is not None:
                return {'status': 'fail', 'message': exec.args[0]}, 200
            return {'status': 'fail', 'message': 'ADD_MARKET_FAILED'}, 200
        return {'status': 'success', 'message': {'market_id': market_id}}, 200
