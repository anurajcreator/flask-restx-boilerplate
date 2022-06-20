from datetime import date,datetime
import json
from app.main.config import response_encryption
from app.main.config import PROJECT_ENVIRONMENT
from app.main.util.v1.encryption import Encryption


def apiresponse(success = "" ,message = "" ,error = None,data =  None, encryption=bool(response_encryption)):

    
    response = {
        'success': success,
        'message': message,
        'data': data,
        'error': error if PROJECT_ENVIRONMENT=='development' else None,
    } 

    if encryption == True:

    #  256 Bytes        32 Bytes      16 Bytes   16 Bytes
       enc_session_key, enc_response, aes_nonce, response_tag = Encryption.encrypt_response(json.dumps(response).encode("utf-8"))

       return f"{str(enc_session_key)}{str(enc_response)}{str(aes_nonce)}{str(response_tag)}"


    return response


    
 
