import threading
from flask import render_template, request
import requests
from app.main.config import FAST2SMS_AUTH_HEADER, FAST2SMS_ROUTE, FAST2SMS_SENDER_ID, FAST2SMS_URL, notification_templates, MAILGUN_API_KEY, MAILGUN_MESSAGES_ENDPOINT, test_server_domain,MAILING_HOST
import os, rq
from redis import Redis
import logging
from app.main.util.v1.apiResponse import apiresponse
from app.main.util.v1.database import save_db


logging_str = "[%(asctime)s: %(levelname)s: %(module)s]: %(message)s"
log_dir = "/tmp/mailgun_service/logs"
os.makedirs(log_dir, exist_ok=True)
logging.basicConfig(filename=os.path.join(log_dir, 'running_logs.log'), level=logging.INFO, format=logging_str,
                    filemode="a")

class MailGun:
    @staticmethod
    def send_mail(email, html, subject, domain=test_server_domain):

        resp = requests.post(MAILGUN_MESSAGES_ENDPOINT,
                            auth=("api", MAILGUN_API_KEY),
                            data={"from": f'{domain}@{MAILING_HOST}',
                                "to": email,
                                "subject": subject,
                                "html": html}
                            )
        return resp

class Email:
    @staticmethod
    def send_email(to, subject, template):
        """Send an email."""
        email = MailGun.send_mail(email=to, html=template, subject=subject)
        if email.status_code == 200:
            return True
        else:
            logging.info("Mail not sent: Error code: {email.status_code}")
            return False

class Fast2SMS:
    def send_sms(phone,message,language='english',flash=0,):
        try:
            request_headers = {

                "authorization":FAST2SMS_AUTH_HEADER,
                "Content-Type":"application/json"
            }

            request_body = {
                'route': FAST2SMS_ROUTE,
                'sender_id': FAST2SMS_SENDER_ID,
                'message': message,
                'language': language,
                'flash': flash,
                'numbers': str(phone)
            }

            sms = requests.request("POST", url=FAST2SMS_URL, headers=request_headers, params=request_body)

            return sms
        except:
            return None

class Notification:
    @staticmethod
    def generate_message(template, data):
        for key, value in data.items():
            find = '{'+key+'}'
            message = template['message'].replace(find,str(value))
            
        return message

    @staticmethod
    def send_notification(template_name, data, receiver=None, credential=None, test=False):
        try:
            
            template = notification_templates[template_name]
            
            if receiver is None:
                if 'email' in template['type'] and 'sms' in template['type']:
                    raise Exception("Reciever is required for both type of notification")
                
                if not credential:
                    raise Exception("Credential is required if reciver is not Provided")
                
                if template['type'] == 'email':
                    receiver_email = credential

                elif template['type'] == 'sms':
                    receiver_phone = credential
                
                else:
                    raise Exception("Invalid Notification Type")
            
            else:
                receiver_email = receiver.email
                receiver_phone = receiver.phone
            
            if not test:
                if template_name == 'forget_password':
                    email_message = Notification.generate_message(template, data[0])
                    sms_message = Notification.generate_message(template, data[1])

                else:   
                    email_message = Notification.generate_message(template, data)
                    sms_message = email_message
            
            elif test:
                email_message = data['message']
                sms_message = email_message
            
            
            for template_type in template['type']:
                if template_type == 'email':
                    if receiver:
                        notification = Notification(
                            user_id = receiver.id,
                            user_role = receiver.role,
                            target = receiver_email,
                            notification_type = template_type,
                            message = email_message,
                            status = 'pending'
                        )

                        save_db(notification)

                        html = render_template(template['html_template'], message=email_message, target = receiver.name)
                    
                    else:
                        html = render_template(template['html_template'], message=email_message)

                    # queue = rq.Queue('generate-notifications', connection=Redis.from_url('redis://'))
                    # queue.enqueue('app.main.util.v1.notification_util.Email.send_email', receiver_email, template['subject'], html)
                    print("email : " + email_message)
                    logging.info(f"Add Email Notification to queue: {template_name}")
                    

                elif template_type == 'sms':
                    if receiver:
                        notification = Notification(
                            user_id = receiver.id,
                            user_role = receiver.role,
                            target = receiver_phone,
                            notification_type = template_type,
                            message = sms_message,
                            status = 'pending'
                        )

                        save_db(notification)
                    # queue = rq.Queue('generate-notifications', connection=Redis.from_url('redis://'))
                    # queue.enqueue('app.main.util.v1.notification_util.Fast2SMS.send_sms', receiver_phone, sms_message)
                    print("sms : " + sms_message)
                    logging.info(f"Add SMS Notification to queue: {template_name}")
                    

                else:
                    raise Exception("Invalid Notification Type")

        except Exception as e:
            logging.info(f"Error sending notification: {e}")
            return apiresponse(False, "Error sending notification")

    def add_notification_to_queue(template_name, data, receiver=None, credential=None, method='rq'):
        try:

            if method== 'rq':
                queue = rq.Queue('generate-notifications', connection=Redis.from_url('redis://'))
                queue.enqueue('app.main.util.v1.notification_util.Notification.send_notification', template_name, data, receiver, credential)
                logging.info(f"Add Notification to queue: {template_name}")
            elif method=='th':
                th = threading.Thread(target=Notification.send_notification, args=(template_name, data, receiver, credential))
                th.start()
                logging.info(f"Create Notification thread: {template_name}")
        except Exception as e:
            logging.warn("Error Occured ")

class TestNotification:
    @staticmethod
    def test_notification(data, user):
        try:
            # resp, status = Auth.get_logged_in_user(request)
            # user = resp['data']

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



    
class Validation:
    @staticmethod
    def validate_email(email: str):
        try:
            address = email.split("@")[0]
            domain = email.split("@")[1]
            service = domain.split(".")[0]
            suffix = domain.split(".")[1]
            return email
        except Exception:
            return False

    @staticmethod       
    def validate_phone(phone: str):
        try:
            if len(phone) == 10:
                try:
                    temp = int(phone)
                    return phone
                except:
                    return False
            else:
                return False
        except Exception:
            return False