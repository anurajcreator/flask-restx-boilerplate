from functools import wraps
from flask import request
from flask.wrappers import Response

from app.main.service.v1.auth_helper import Auth
from app.main.util.v1.apiResponse import apiresponse

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        response, status = Auth.get_logged_in_user(request)
        token = response.get('data')
        if token == None:
            return response, status

        return f(*args, **kwargs)

    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        response, status = Auth.get_logged_in_user(request)
        print(response)
        token = response.get('data')
        print(token)
        
        if token == None:
            return response, status
        
        role = token['role']
        if role != 'admin':
            return apiresponse(False, 'Admin Access Required', 'Admin Access Required', None)
        
        return f(*args, **kwargs)
    
    return decorated
