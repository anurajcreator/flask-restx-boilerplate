from flask_restx import Namespace, fields

class UserDto:
    api = Namespace('user', description='user related operations')
    
    test_notification = api.model('test_notification',{
        'message': fields.String(required=True)
    })