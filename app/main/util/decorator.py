from functools import wraps
from flask import request
from flask.wrappers import Response

from app.main.service.auth_helper import Auth
from app.main.util.apiResponse import apiresponse

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        response, status = Auth.get_logged_in_user(request)
        token = response.get('data')
        if token == 'null':
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
        
        if token == 'null':
            return response, status
        
        role = token['role']
        if role != 'admin':
            return apiresponse('false', 'Admin Access Required', 'Admin Access Required', 'null')
        
        return f(*args, **kwargs)
    
    return decorated
