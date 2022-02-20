from app.main.util.v1.decorator import token_required
from flask import request
from flask_restx import Resource
from app.main.service.v1.user_helper import User
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
    def post(self):
        return User.test_notification(data=request.json)
