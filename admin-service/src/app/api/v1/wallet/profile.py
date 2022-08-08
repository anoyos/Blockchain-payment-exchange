from flask_restful import reqparse, Resource
from app import app
from app.api.v1.market.common import Token
from connectors.v2.wallet import celery_Wallet
from uuid import UUID

class api_v1_admin_currency_profile(Resource):
    # Expecting that Admin Bearer token is included in the
    # Authorization header. Returns data about the queried user.
    # {
    #   "currencyid": "currencyid",
    # }

    def get(self):
        return {}, 200

    def post(self):
        session = Token().verify_session()
        if not session:
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200    
        if not session.get('admin'):
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200
        
        parser = reqparse.RequestParser()
        parser.add_argument("currencyid", type=str)
        args = parser.parse_args()

        try:
            currencyid = UUID(args['currencyid'], version=4)
        except Exception:
            return {"status": "fail", "message": "ERR_INVALID_CURRENCYID"}, 200

        message = {
            'currencyid': str(args.get('currencyid')),
            'basic': False,
            'names': False,
            'admin': True,
            'backend': False,
        }
        wc = celery_Wallet()
        result = wc.c.get_wallet_profile.apply_async(
            args=[message], queue=app.config['Q_WALLET_CONN'])

        try:
            returndata = result.get(5)
            
        except Exception:
            return {
                'status': 'fail',
                'message': 'ERR_WALLET_CONN_UNAVAILABLE',
            }, 200
            
        return {
            'status': 'success',
            'message': returndata,
        }, 200
        
        currency = rpc.call()
        return currency, 200

