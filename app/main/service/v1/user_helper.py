

from flask import request
from app.main.service.v1.auth_helper import Auth
from flask import request
from app.main.util.v1.apiResponse import apiresponse
from app.main.util.v1.notification_util import Notification

class User:
    def test_notification(data):
        try:
            user, resp = Auth.get_logged_in_user(request)
            user = user['data']

            try:
                Notification.send_notification("test", data, receiver=user,test=True)

                response = apiresponse("True", "Notification queued successfully!", None, data)

                return response, 200
            except Exception as e:
                error = apiresponse("False", "Error Sending Notification", str(e), None)
                return error, 500
        except Exception as e:
            error = apiresponse("False", "Something went wrong", str(e), None)
            return error, 500
    
