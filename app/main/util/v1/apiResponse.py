from datetime import date,datetime
from flask import request


def apiresponse(success = "" ,message = "" ,error = 'null',data =  'null' ):

    return {
    "success": success,
    "message": message,
    "data": data,
    "error": error,
}


def date_to_str(date):
    if date:
        return str(date.day) + "-" + str(date.month) + "-" + str(date.year)
    else:
        return ""

def str_to_date(data):
    n_date = data.split("-")
    data = datetime(int(n_date[0]),int(n_date[1]),int(n_date[2]))
    return data
    
 
