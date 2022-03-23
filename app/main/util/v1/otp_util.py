import random
import logging as log
import datetime as dt
from app.main.config import key
from app.main.model.otp import Otp
from app.main.util.v1.apiResponse import apiresponse
from app.main.util.v1.database import save_db
import jwt
class OTPUtil:
    
    @staticmethod
    def get_otp(credential, credential_type, otp_type):
        try:
            _otp = Otp.query.filter_by(credential = credential).filter_by(credential_type = credential_type).filter_by(otp_type = otp_type).filter_by(deleted_at = None).first()
            if _otp:

                if _otp.restriction_time:
                    if _otp.restriction_time > dt.datetime.utcnow():
                        remaining_time = (_otp.restriction_time - dt.datetime.utcnow()).minute
                        return apiresponse(False, "Maximum Attempts reached, wait for {} minutes".format(remaining_time), encryption=False)

                # if _otp.expire_at < dt.datetime.utcnow():
                #     otp = OTPUtil.generate_otp(credential)
                #     _otp.otp = otp
    
                if _otp.counter > 3:
                    _otp.counter = 0

                otp = OTPUtil.generate_otp()
                _otp.otp = otp
                _otp.expire_at =  dt.datetime.utcnow()+dt.timedelta(minutes=30)    
            
            else:
                otp = OTPUtil.generate_otp()
                   
                _otp = Otp(
                    credential = credential,
                    credential_type = credential_type,
                    otp = otp,
                    # user_id = user_obj.id,
                    # user_role = user_obj.role,
                    otp_type = otp_type,
                    restriction_time = dt.datetime.utcnow(),
                    expire_at = dt.datetime.utcnow()+dt.timedelta(minutes=30)
                )

            save_db(_otp)
                
            return apiresponse(True,None,None, str(otp), encryption=False) 


        except Exception as e:
            log.error('OTP Gen : %s', str(e))
            raise e

    @staticmethod
    def check_otp(otp_num , credential, credential_type, otp_type):
        try:
            otp = Otp.query.filter_by(credential = credential).filter_by(otp_type = otp_type).filter_by(credential_type = credential_type).filter_by(deleted_at = None).first()
            
            if not otp:
                return apiresponse(False, f"No Record Found for {credential_type} {credential}", encryption=False)

            if otp.expire_at < dt.datetime.utcnow():
                return apiresponse(False, f"Otp Expired for {credential_type} {credential}", encryption=False)
            
            if otp.counter > 3:
                otp.deleted_at = dt.datetime.utcnow()
                save_db(otp)
                return apiresponse(False, f"Maximum Otp Limit exceded for {credential_type} {credential}", encryption=False)  
            
            if otp.check_otp(otp_num):
                payload = {
                    'otp' : otp_num,
                    'credential' : credential,
                    'iat': dt.datetime.utcnow(),
                    'exp' : dt.datetime.utcnow()+dt.timedelta(minutes=30),
                }

                token = jwt.encode(payload, key, algorithm='HS256')
                otp.verified_at = dt.datetime.utcnow()
                otp.deleted_at = dt.datetime.utcnow()
                otp.otp_token = token
                save_db(otp)

                return apiresponse(True, "Otp verified", None, token, encryption=False)
                
            else:
                otp.counter += 1
                return apiresponse(False, f"Wrong OTP Provided for {credential_type} {credential}", None, encryption=False)
            

        except Exception as e:
            log.error('OTP Check : %s', str(e))
            raise e

    @staticmethod
    def generate_otp():
        try:
            otp = int(dt.datetime.now().strftime("%f")) + random.randint(100000, 999999)
            while otp < 100000:
                otp = int(dt.datetime.now().strftime("%f")) + random.randint(100000, 999999)

            while len(str(otp)) > 6:
                otp = int(str(otp)[1:])
            
            return str(otp)

        except Exception as e:
            log.error('OTP Gen : %s', str(e))

    @staticmethod
    def check_token(credential,token):
        try:
            payload = jwt.decode(token, key, algorithms=['HS256'])
            
            if payload['credential'] == credential:
                _otp = Otp.query.filter_by(credential = credential).filter_by(otp_token = token).filter_by(deleted_at = None).first()
                if not _otp:
                    return apiresponse(False, f"No Record Found for {credential} with token {token}", encryption=False)
                return True
            else:
                return 'Invalid Credential Token'

        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except  jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'