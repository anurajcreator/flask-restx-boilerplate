from datetime import date,datetime
import json
from flask import request

from app.main.util.v1.encryption import Encryption


def apiresponse(success = "" ,message = "" ,error = 'null',data =  'null', encryption=False ):

    response = {
        "success": success,
        "message": message,
        "data": data,
        "error": error,
    } 

    if encryption == True:

    #  256 Bytes        32 Bytes      16 Bytes   16 Bytes
       enc_session_key, enc_response, aes_nonce, response_tag = Encryption.encrypt_data(json.loads(response).encode("utf-8"))

       return f"{enc_session_key}{enc_response}{aes_nonce}{response_tag}"


    return response


    
 
