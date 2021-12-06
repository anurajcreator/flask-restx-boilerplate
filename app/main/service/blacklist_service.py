from app.main import db 
from app.main.model.blacklist import BlacklistToken
from app.main.util.apiResponse import apiresponse

def save_token(token):
    try:
        blacklist_token = BlacklistToken(token = token)
        try:
            #insert the token
            db.session.add(blacklist_token)
            db.session.commit()
            return apiresponse("success",'Successfuly logged out', 'null' , "null"), 200
        except Exception as e:
            response_object = {
                'status':'fail',
                'message':e
            }
            return apiresponse("fail",'Fail to Logout', str(e) , "null"), 200
    except Exception as e:
        return apiresponse("false","Internal Server Error",str(e), "null"), 500