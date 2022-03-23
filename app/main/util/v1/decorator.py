from functools import wraps
from flask import request
from flask.wrappers import Response

from app.main.service.v1.auth_helper import Auth
from app.main.util.v1.apiResponse import apiresponse

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        resp, status = Auth.get_logged_in_user(request)
        user = resp['data']
        if user == None:
            return resp, status

        return f(*args, **kwargs)

    return decorated

def admin_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        resp, status = Auth.get_logged_in_user(request)
        user = resp['data']
        
        if user == None:
            return resp, status
        
        role = user.role
        if role != 'admin':
            return apiresponse(False, 'Admin Access Required', 'Admin Access Required', None)
        
        return f(*args, **kwargs)
    
    return decorated
