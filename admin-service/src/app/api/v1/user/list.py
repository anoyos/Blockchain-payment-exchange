from flask import request
from flask_restful import reqparse, Resource
from app import app
from app.api.v1.market.common import Token
from app.api.v1.market.common import Rpc


class api_v1_admin_user_list(Resource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.

    def get(self):
        return {}, 200

    def post(self):
        session = Token().verify_session()
        if not session:
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200    
        if not session.get('admin'):
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200


        parser = reqparse.RequestParser()
        parser.add_argument("page", type=int)
        parser.add_argument("perpage", type=int)
        payload = parser.parse_args()

        headers = {
            "Content-Type": "Application/json",
            "Authorization": request.headers.get("Authorization"),
        }

        user = Rpc(
            host=app.config["AUTH_SERVICE_HOST"],
            port=app.config["AUTH_SERVICE_PORT"],
            uri="/api/v1/user/internal/user/list/",
            payload=payload,
            headers=headers,
        ).call()

        return user, 200
