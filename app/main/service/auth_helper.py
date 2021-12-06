from app.main.model.user import User
from app.main.service.blacklist_service import save_token
from app.main.util.apiResponse import apiresponse
from app.main import db

import datetime

class Auth:

    @staticmethod
    def login_user(data):
        try:
            # fetch the user data
            user = User.query.filter_by(email=data.get('email')).first()
            if not user:
                user = User.query.filter_by(username=data.get('email')).first()
            if user: 
                if user.check_password(data.get('password')):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        data = {
                            'username': user.username,
                            'email':user.email, 
                            'Authorization': auth_token
                        }
                        return apiresponse("true",'Successfully logged in', "null", data), 200
                else:
                    return apiresponse("false",'Email or Password does not match.', "Email or Password does not match.", "null"), 401
            else:
                return apiresponse("false",'User Not found.', "User Not found.", "null"), 404

        except Exception as e:
            return apiresponse("false",'Try again',str(e), "null"), 500

    @staticmethod
    def logout_user(new_request):
        auth_token = new_request.headers.get('Authorization')
        try:
            # print(auth_token)
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    # mark the token as blacklisted
                    return save_token(token=auth_token)
                else:
                    return apiresponse("false","Invalid User Please Login First", resp , "null"), 401
            else:
                return apiresponse("false",'Invalid User Please Login First', 'Provide a valid auth token.' , "null"), 403
        except Exception as e:
            return apiresponse("false","Internal Server Error",str(e), "null"), 500
    
    @staticmethod
    def get_logged_in_user(new_request):
        #get the auth token
        try:
            auth_token = new_request.headers.get('Authorization')
            # print(auth_token)
            if auth_token:
                resp = User.decode_auth_token(auth_token)
                if not isinstance(resp, str):
                    user = User.query.filter_by(id=resp).first()
                    data = {
                        'username': user.username,
                        'email' : user.email,
                        'role': user.role,
                        'registered_on': str(user.registered_on)
                    }
                    return apiresponse("true", 'Logged in User Found','null' ,data), 200
                return apiresponse('false', 'Invalid User Please Login First', resp, 'null'), 401
            else:
                return apiresponse('false','Invalid User Please Login First', 'Provide a valid auth token', 'null'),401
        except Exception as e:
            return apiresponse("false","Internal Server Error",str(e), "null"), 500

    @staticmethod
    def save_new_user(data):
        try:
            user = User.query.filter_by(email=data['email']).first()
            if user:
                return apiresponse("false","User with same email allready exists","User with same email allready exists","null"), 409
            else:
                user = User.query.filter_by(username=data['username']).first()
                if user:
                    return apiresponse("false", "User with same Username allready exists","User with same Username allready exists","null"), 409
                else:
                    new_user = User(
                        email=data['email'],
                        username=data['username'],
                        password=data['password'],
                        role = data['role'],
                        registered_on=datetime.datetime.utcnow()
                    )
                    try:
                        Auth.save_changes(new_user)
                        return Auth.generate_token(new_user)

                    except Exception as e:
                        db.session.rollback()
                        db.session.commit()
                        return apiresponse('false','Unknow Error', str(e),"null"), 400
        
        except Exception as e:
            return apiresponse("false","Internal Server Error",str(e),"null"), 500

    
    def save_changes(data):
        db.session.add(data)
        db.session.commit()

    def generate_token(user):
        try:
            #genarate the auth token
            auth_token = user.encode_auth_token(user.id)
            data = {
                    'username': user.username,
                    'email':user.email,
                    'role' : user.role,
                    'id' : user.id, 
                    'Authorization': auth_token
                    }
            return apiresponse("true",'Successfully Registered', "null", data), 200
        except Exception as e:
            return apiresponse("False", "Some Error Occurred. Please Try Again",str(e)), 401  