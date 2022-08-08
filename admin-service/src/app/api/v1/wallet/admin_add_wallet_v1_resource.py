from bullflag_commons.flask.bullflag_secure_resource import BullflagSecureAdminResource
from bullflag_commons.logging import get_logger
from flask_restful import abort, Resource, reqparse


class AdminAddWalletV1Resource(BullflagSecureAdminResource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.

    logger = get_logger(__name__)

    def __init__(self, **kwargs):
        self._wallet_service = kwargs['wallet_service']
        super(AdminAddWalletV1Resource, self).__init__(kwargs['token_service'])

    def get(self):
        abort(400)

    def post(self):
        session_check = super(AdminAddWalletV1Resource, self).check_session()
        if not session_check.is_good:
            return session_check.rest_response

        try:
            parser = reqparse.RequestParser()
            parser.add_argument("confirmations", required = True)
            parser.add_argument("currency_short_name", required = True)
            parser.add_argument("currency_name", required = True)
            parser.add_argument("currency_type", required = True)
            parser.add_argument("username", required = True)
            parser.add_argument("password", required = True)
            parser.add_argument("wallet_port_rpc", required = True)
            parser.add_argument("wallet_port_p2p", required = True)
            parser.add_argument("wallet_host", required = True)
            parser.add_argument("wallet_host_backup", required = True)
            parser.add_argument("withdrawal_fee", required = True)
            parser.add_argument("wpassword", required = True)
            args = parser.parse_args()

            if self._wallet_service.wallet_exists(args['currency_short_name']):
                return {"status": "success", "message": "CURRENCY_ALREADY_EXISTS"}, 200
            else:
                currency_id = self._wallet_service.create_new_wallet(dict(args))
                payload = {"currency_id": currency_id}
        except Exception as exec:
            self.logger.info("Bad request {}".format(exec), exc_info = exec)
            return
        return {"status": "success", "message": "CURRENCY_CREATED", "payload": payload}, 200
