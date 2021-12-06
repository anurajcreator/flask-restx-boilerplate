from app.main.util.decorator import token_required
from flask import request
from flask_restx import Resource

from app.main.service.auth_helper import Auth
from app.main.util.authDto import AuthDto

from ..util.decorator import token_required
from ..service.auth_helper import Auth

api = AuthDto.api 
user_auth = AuthDto.user_auth
_user_create = AuthDto.create_user

@api.route('/login')
class UserLogin(Resource):
    """
    User Login Resource
    """
    @api.doc('user login')
    @api.expect(user_auth, validate=True)
    def post(self):
        """Logs in existing users"""
        #get post data
        post_data = request.json
        return Auth.login_user(data=post_data)

@api.route('/logout')
class LogoutAPI(Resource):
    """
    Logout Resource
    """
    @api.doc('logout a user')
    @api.doc(security='apikey')
    @token_required
    def post(self):

        #get auth token
        
        # auth_header = request.headers.get('Authorization')

        return Auth.logout_user(request)
        """Logs out the current user """
        return Auth.logout_user(request)


@api.route('/register')
class UserRegister(Resource):
    @api.response(201, 'User successfully created.')
    @api.response(409, 'User already exists. Please Log in.')
    @api.doc('Register a New User')
    @api.expect(_user_create,validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return Auth.save_new_user(data=data)

