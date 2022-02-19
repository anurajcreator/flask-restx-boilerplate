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
                if _otp.expire_at < dt.datetime.utcnow():
                        otp = OTPUtil.generate_otp(credential)
                        _otp.otp = otp
    
                if _otp.counter > 3:
                    otp = OTPUtil.generate_otp()
                    _otp.otp = otp
                    _otp.counter = 0

                _otp.expire_at =  dt.datetime.utcnow()+dt.timedelta(hours=1)    
            
            else:
                otp = OTPUtil.generate_otp()
                   
                _otp = Otp(
                    credential = credential,
                    credential_type = credential_type,
                    otp = otp,
                    # user_id = user_obj.id,
                    # user_role = user_obj.role,
                    otp_type = otp_type,
                    expire_at = dt.datetime.utcnow()+dt.timedelta(hours=6)
                )

            save_db(_otp)
                
            return str(_otp.otp)


        except Exception as e:
            log.error('OTP Gen : %s', str(e))
            raise e

    @staticmethod
    def check_otp(otp_num , credential, credential_type, otp_type):
        try:
            otp = Otp.query.filter_by(credential = credential).filter_by(otp_type = otp_type).filter_by(credential_type = credential_type).filter_by(deleted_at = None).first()
            
            if not otp:
                return apiresponse(False, "No Record Found")
            
            if otp.expire_at < dt.datetime.utcnow():
                return apiresponse(False, "Otp Expired")
            
            if otp.counter > 3:
                otp.deleted_at = dt.datetime.utcnow()
                save_db(otp)
                return apiresponse(False, "Maximum Otp Limit exceded")  
            
            if Otp.check_otp(otp_num):
                payload = {
                    'otp' : otp_num,
                    'credential' : credential,
                    'verified_at' : str(dt.datetime.utcnow()),
                }

                token = jwt.encode(payload, key, algorithm='HS256')
                otp.verified_at = dt.datetime.utcnow()
                otp.deleted_at = dt.datetime.utcnow()
                save_db(otp)

                return apiresponse(True, "Otp verified", None, token)
                
            else:
                otp.counter += 1
                return apiresponse(False, "Wrong OTP Provided", None)
            

        except Exception as e:
            log.error('OTP Check : %s', str(e))
            raise e

    @staticmethod
    def generate_otp():
        try:
            otp = int(dt.datetime.now().strftime("%f")) + random.randint(100000, 999999)
            
            while len(str(otp)) > 6:
                otp = int(str(otp)[1:])
            
            return str(otp)

        except Exception as e:
            log.error('OTP Gen : %s', str(e))
