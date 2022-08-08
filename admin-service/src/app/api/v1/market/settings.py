
from flask_restful import Resource


class api_v1_admin_market_setting_enable(Resource):
    # Expecting that Admin Bearer token is included in the Authorization
    # header. Returns data about the queried user.
    # {
    #    'marketid': '888c4dd9-46e5-4198-b73f-f68b0c01f680'
    # }
    def get(self):
        return {}, 200

    def post(self, settings=None, enable=None):
        session = Token().verify_session()
        if not session:
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200    
        if not session.get('admin'):
            return {"status": "fail", "message": "ERR_INVALID_REQUEST"}, 200

        return {'status': 'fail', 'message': 'ERR_DEPRICATED'}