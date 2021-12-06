from flask_restx import Namespace, fields

class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True,description='The email address'),
        'password':fields.String(required=True,description='The use password')
    })

    create_user = api.model('create_user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'role': fields.String(required=True, description='user role')
    })
    

