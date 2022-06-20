from flask_restx import Namespace, fields

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True,description='The email address'),
        'password':fields.String(required=True,description='The use password'),
    })

    send_otp = api.model('send_otp', {
        'email': fields.String(required=True,description='The email address'),
        'phone':fields.String(required=True,description='The phone number'),
    })

    verify_sign_up_otp = api.model('verify_sign_up_otp', {
        'email': fields.String(required=True,description='The email address'),
        'phone':fields.String(required=True,description='The phone number'),
        'email_otp':fields.String(required=True,description='The otp'),
        'phone_otp':fields.String(required=True,description='The otp'),
    })

    forget_password = api.model('forget_password', {
        'email': fields.String(required=True,description='The email address'),
        'phone':fields.String(required=True,description='The phone number'),
        'email_otp':fields.String(required=True,description='The otp'),
        'phone_otp':fields.String(required=True,description='The otp'),
        'password':fields.String(required=True,description='The use password'),
    })

    create_user = api.model('create_user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'private_1': fields.String(required=True, description='user role')
    })
