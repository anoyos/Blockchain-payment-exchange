from flask import request
from flask_restful import reqparse, abort, Resource
from app import app
from common.crypto import Token
from connectors.v2.market import celery_Market


class api_v1_admin_market_list(Resource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.

    def get(self, basecurrencyid=None):
        return {}, 200

    def post(self, basecurrencyid=None):
        session = Token().verify_session()

        if not session and not session.get("admin"):
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200

        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int)
        parser.add_argument("perpage", type=int)
        parser.add_argument("option", type=str)
        args = parser.parse_args()

        option = 'all' if not args.get('option') else args['option']

        valid_options = [
            'all',
            'enabled',
            'disabled',
            'featured',
        ]
        try:
            if option not in valid_options:
                raise Exception("Invalid list option")
        except Exception:
            print("Invalid list option")
            print("")
            print(valid_options)
            print("")
            return {"status": "fail", "message": valid_options}, 200
        mc = celery_Market()
        result = mc.c.market_list.apply_async(
            args=[{}], queue=app.config['Q_MARKET_CONN'])
        try:
            markets = result.get(5)
        except Exception as exc:
            print("Failed: {}".format(exc))
            return {"status": "fail", "message": "ERR_MC_UNAVAILABLE"}, 200

        if not isinstance(markets, list):
            print("The query failed")
            return {"status": "fail", "message": markets}, 200

        return {"status": "success", "message": markets}, 200