import jwt
from app.main.model.blacklist import BlacklistToken
from app.main.model.user import User
from app.main.service.v1.blacklist_service import save_token
from app.main.util.v1.apiResponse import apiresponse
from app.main import db
from app.main.config import key
import datetime
from app.main.util.v1.database import save_db
from app.main.util.v1.notification_util import Notification, Validation
from app.main.util.v1.otp_util import OTPUtil

class Auth:

    user_class = {
        'user' : User
    }

    @staticmethod
    def get_user(id , role):
        user = Auth.user_class[role].query.filter_by(id = id).first()
        
        return user
    
    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = Auth.user_class[data['role']].query.filter_by(email=data['email']).first()
            if not user:
                user = User.query.filter_by(username=data['email']).first()
            if user: 
                if user.check_password(data['password']):
                    auth_token = user.encode_auth_token()
                    if auth_token:
                        data = {
                            'Authorization': auth_token
                        }
                        return apiresponse(True,'Successfully logged in', None, data), 200
                else:
                    return apiresponse(False,'Email or Password does not match.', "Email or Password does not match.", None), 401
            else:
                return apiresponse(False,'User Not found.', "User Not found.", None), 404

        except Exception as e:
            return apiresponse(False,'Try again',str(e), None), 500

    @staticmethod
    def logout_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        try:
            # print(auth_token)
            if auth_token:
                resp = Auth.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    # mark the token as blacklisted
                    return save_token(token=auth_token)
                else:
                    return apiresponse(False,"Invalid User Please Login First", resp , None), 401
            else:
                return apiresponse(False,'Invalid User Please Login First', 'Provide a valid auth token.' , None), 403
        except Exception as e:
            return apiresponse(False,"Internal Server Error",str(e), None), 500
    
    @staticmethod
    def get_logged_in_user(new_request):
        #get the auth token
        try:
            auth_token = new_request.headers.get('Authorization')
            # print(auth_token)
            if auth_token:
                resp = Auth.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    user = Auth.user_class[resp['role']].query.filter_by(id=resp['id']).first()
                    return apiresponse(True, 'Logged in User Found',None ,user), 200

                return apiresponse(False, 'Invalid User Please Login First', resp, None), 401
            else:
                return apiresponse(False,'Invalid User Please Login First', 'Provide a valid auth token', None),401
        except Exception as e:
            return apiresponse(False,"Internal Server Error",str(e), None), 500
    
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token,key,algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except  jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    @staticmethod
    def send_sign_up_otp(data):
        try:
            email = Validation.validate_email(data['email'])
            phone = Validation.validate_phone(data['phone'])

            if not email:
                return apiresponse(False, 'Invalid Email', None, None), 400

            if not phone:
                return apiresponse(False, 'Invalid Phone', None, None), 400
                
            email_otp = OTPUtil.get_otp(email, 'email', 'signup')

            if email_otp['success'] == True:
                email_otp = email_otp['data']
            
            else:
                return apiresponse(False, email_otp['message']), 400

            phone_otp = OTPUtil.get_otp(phone, 'phone', 'signup')

            if phone_otp['success'] == True:
                phone_otp = phone_otp['data']
            
            else:
                 return apiresponse(False, phone_otp['message']), 400

            Notification.send_notification('otp_signup_email', {'otp': email_otp},None, email)
            Notification.send_notification('otp_signup_phone', {'otp': phone_otp},None, phone)

            # return apiresponse(True, 'OTP sent Successfully', None, None), 200
            return apiresponse(True, 'OTP sent Successfully', None, {'email_otp' : email_otp, 'phone_otp' : phone_otp}), 200

        except Exception as e:
            return apiresponse(False,"Internal Server Error",str(e), None), 500

    @staticmethod
    def verify_sign_up_otp(data):
        try:
            email = Validation.validate_email(data['email'])
            phone = Validation.validate_phone(data['phone'])

            if not email:
                return apiresponse(False, 'Invalid Email', None, None), 400

            if not phone:
                return apiresponse(False, 'Invalid Phone', None, None), 400

            email_otp = OTPUtil.check_otp(data['email_otp'],email, 'email', 'signup')
            if email_otp['success'] == True:
                email_token = email_otp['data']
            
            else:
                return apiresponse(False, email_otp['message']), 400

            phone_otp = OTPUtil.check_otp(data['phone_otp'],phone, 'phone', 'signup')
            if phone_otp['success'] == True:
                phone_token = phone_otp['data']
            
            else:
                return apiresponse(False, phone_otp['message']), 400

            return apiresponse(True, 'OTP Verified Successfully', None, {'email_token' : email_token, 'phone_token' : phone_token}), 200

        except Exception as e:
            return apiresponse(False,"Internal Server Error",str(e), None), 500

    @staticmethod
    def forget_password_send_otp(data):
        try:
            email = Validation.validate_email(data['email'])
            phone = Validation.validate_phone(data['phone'])

            if not email:
                return apiresponse(False, 'Invalid Email', None, None), 400

            if not phone:
                return apiresponse(False, 'Invalid Phone', None, None), 400

            email_otp = OTPUtil.get_otp(email, 'email', 'forget_password')

            if email_otp['success'] == True:
                email_otp = email_otp['data']
            
            else:
                return apiresponse(False, email_otp['message']), 400

            phone_otp = OTPUtil.get_otp(phone, 'phone', 'forget_password')

            if phone_otp['success'] == True:
                phone_otp = phone_otp['data']
            
            else:
                return apiresponse(False, phone_otp['message']), 400

            user = Auth.user_class[data['user_role']].query.filter_by(email=email).filter_by(phone=phone).filter_by(deleted_at = None).first()

            if not user:
                return apiresponse(False, 'User Not Found', None, None), 400
            
            Notification.send_notification('otp_forget_password',[{'otp' : email_otp}, {'otp' : phone_otp}],user)
            

            # return apiresponse(True, 'OTP sent Successfully', None, None), 200
            return apiresponse(True, 'OTP sent Successfully', None, {'email_otp' : email_otp, 'phone_otp' : phone_otp}), 200

        except Exception as e:
            return apiresponse(False,"Internal Server Error",str(e), None), 500

    @staticmethod
    def forget_password_verify(data):
        try:
            email = Validation.validate_email(data['email'])
            phone = Validation.validate_phone(data['phone'])

            if not email:
                return apiresponse(False, 'Invalid Email', None, None), 400

            if not phone:
                return apiresponse(False, 'Invalid Phone', None, None), 400

            email_otp = OTPUtil.check_otp(data['email_otp'],email, 'email', 'forget_password')
            if email_otp['success'] == True:
                email_token = email_otp['data']
            
            else:
                return apiresponse(False, email_otp['message']), 400

            phone_otp = OTPUtil.check_otp(data['phone_otp'],phone, 'phone', 'forget_password')
            if phone_otp['success'] == True:
                phone_token = phone_otp['data']
            
            else:
                return apiresponse(False, phone_otp['message']), 400

            user = Auth.user_class[data['user_role']].query.filter_by(email=email).filter_by(phone=phone).filter_by(deleted_at = None).first()

            if not user:
                return apiresponse(False, 'User Not Found', None, None), 400
            
            user.password = data['password']

            save_db(user)

            Notification.send_notification('forget_password_success',{'key':None},user)
            
            return apiresponse(True, 'Password Changed Successfully', None, None), 200
            
        except Exception as e:
            return apiresponse(False,"Internal Server Error",str(e), None), 500