from flask import request
from flask_restful import reqparse, Resource
from app import app
from app.api.v1.market.common import Token
from app.api.v1.market.common import Rpc


class api_v1_admin_user_profile(Resource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.
    # {
    #   "userid": "userid of user profile",
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
        parser.add_argument("userid")
        args = parser.parse_args()
        payload = {
            "userid": args["userid"]
            if args["userid"]
            else session.get("userid"),
            "fromadmin": True,
        }
        headers = {
            "Content-Type": "Application/json",
            "Authorization": request.headers.get("Authorization"),
        }

        # We do not have the data ourselves, forwarding the
        # request to auth service.
        rpc = Rpc(
            host=app.config["AUTH_SERVICE_HOST"],
            port=app.config["AUTH_SERVICE_PORT"],
            uri="/api/v1/user/profile/full/",
            payload=payload,
            headers=headers,
        )

        user = rpc.call()
        return user, 200

