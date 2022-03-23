from app.main.util.v1.decorator import token_required
from flask import request
from flask_restx import Resource

from app.main.service.v1.auth_helper import Auth
from app.main.util.v1.authDto import AuthDto

from ....util.v1.decorator import token_required
from ....service.v1.auth_helper import Auth

api = AuthDto.api 
user_auth = AuthDto.user_auth
_user_create = AuthDto.create_user
send_otp = AuthDto.send_otp
verify_sign_up_otp = AuthDto.verify_sign_up_otp
forget_password = AuthDto.forget_password

@api.route('/sign_up_otp/send')
class SendSignUpOtp(Resource):
    @api.doc('Send Signup OTP')
    @api.expect(send_otp, validate=True)
    def post(self):
        """ Send Signup OTP """
        data = request.json
        return Auth.send_sign_up_otp(data)

@api.route('/sign_up_otp/verify')
class VerifySignUpOtp(Resource):
    @api.doc('Verify Signup OTP')
    @api.expect(verify_sign_up_otp, validate=True)
    def post(self):
        """ Verify Signup OTP """
        data = request.json
        return Auth.verify_sign_up_otp(data)

@api.route('/forget_password/send')
class SendForgetPasswordOtp(Resource):
    @api.doc('Send Forget Password OTP')
    @api.expect(send_otp, validate=True)
    def post(self):
        """ Send Forget Password OTP """
        data = request.json
        return Auth.send_forget_password_otp(data)

@api.route('/forget_password/verify')
class VerifyForgetPasswordOtp(Resource):
    @api.doc('Verify Forget Password OTP')
    @api.expect(forget_password, validate=True)
    def post(self):
        """ Verify Forget Password OTP """
        data = request.json
        return Auth.verify_forget_password_otp(data)

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
        return Auth.logout_user(request)
       