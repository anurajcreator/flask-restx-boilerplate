from app.main.util.v1.decorator import token_required
from flask import request
from flask_restx import Resource
from app.main.util.v1.notification_util import Notification
from app.main.util.v1.userDto import UserDto
from ....util.v1.decorator import token_required


api = UserDto.api


@api.route('/test_notification')
class UserLogin(Resource):
    """
    User Notification Test Resource
    """
    @api.doc('user login')
    @api.expect(UserDto.test_notification, validate=True)
    @token_required
    @api.doc(security='apikey')
    def post(self):
        return Notification.test_notification(data=request.json)
