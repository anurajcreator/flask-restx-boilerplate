from datetime import date,datetime,timedelta,time
from flask import request
from app.main import db
import pytz

#TIMEZONE SETTINGS
IST = pytz.timezone('Asia/Kolkata')



def date_to_str(date):
    if date:
        if date.day < 10 :
            day = "0" + str(date.day)
        else:
            day = str(date.day)
        if date.month <10 :
            month = "0" + str(date.month)
        else:
            month = str(date.month)
        return day + "-" + month + "-" + str(date.year)
    else:
        return ""

def str_to_date(data):
    if data != "":
        n_date = data.split("-")
        try:
            date = datetime(int(n_date[0]),int(n_date[1]),int(n_date[2]))
        except:
            date = datetime(int(n_date[2]),int(n_date[1]),int(n_date[0]))
        return date

def time_to_str(time):
    if time:
        if time.hour < 10 :
            hour = "0" + str(time.hour)
        else:
            hour = str(time.hour)
        if time.minutes <10 :
            minutes = "0" + str(time.minute)
        else:
            minutes = str(time.minutes)
        return hour + ":" + minutes
    else:
        return ""
    
def str_to_time(data):
    if data == "" or len(data) > 5 or ':' not in data:
        raise Exception(f'{data} is not in "HH:MM" format')
    
    n_time = data.split(":")
    
    if not isinstance(n_time[0], int):
        raise Exception(f'Hour : {n_time[0]} in {data} should be an integer')
    
    if not isinstance(n_time[1], int):
        raise Exception(f'Minute : {n_time[1]} is {data} should be an integer')
    
    
    return_time = time(n_time[0],n_time[1])
    return return_time

def datetime_to_str(datetime):
    if datetime:
        if datetime.day < 10 :
            day = "0" + str(datetime.day)
        else:
            day = str(datetime.day)
        if datetime.month <10 :
            month = "0" + str(datetime.month)
        else:
            month = str(datetime.month)
        return day + "-" + month + "-" + str(datetime.year) + " " + time_to_str(datetime.time())
    else:
        return ""


def if_datetime(data):
    if data:
        return datetime_to_str(data)
    else:
        return None

def if_date(data):
    if data:
        return date_to_str(data)
    else:
        return None

def if_time(time):
    if time:
        return time_to_str(time)
    else:
        return None

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
