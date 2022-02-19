from datetime import date,datetime
from flask import request


def apiresponse(success = "" ,message = "" ,error = 'null',data =  'null' ):

    return {
    "success": success,
    "message": message,
    "data": data,
    "error": error,
}


    
 
