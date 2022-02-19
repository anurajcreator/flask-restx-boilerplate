from flask import render_template
import requests
from app.main.config import FAST2SMS_AUTH_HEADER, FAST2SMS_ROUTE, FAST2SMS_SENDER_ID, FAST2SMS_URL, notification_templates, MAILGUN_API_KEY, MAILGUN_MESSAGES_ENDPOINT, test_server_domain,MAILING_HOST
import os
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
    def send_notification(template_name, data, reciever=None, credential=None):
        try:
            template = notification_templates[template_name]
            
            if reciever is None:
                if 'email' in template['type'] and 'sms' in template['type']:
                    raise Exception("Reciever is required for both type of notification")
                
                if not credential:
                    raise Exception("Credential is required if reciver is not Provided")
                
                if template['type'] == 'email':
                    reciever_email = credential

                elif template['type'] == 'sms':
                    reciever_phone = credential
                
                else:
                    raise Exception("Invalid Notification Type")
            
            else:
                reciever_email = reciever.email
                reciever_phone = reciever.phone

            message = Notification.generate_message(template, data)
            
            for template_type in template['type']:
                if template_type == 'email':
                    if reciever:
                        notification = Notification(
                            user_id = reciever.id,
                            user_role = reciever.role,
                            target = reciever_email,
                            notification_type = template_type,
                            message = message,
                            status = 'pending'
                        )

                        save_db(notification)
                    html = render_template(template['html_template'], message=message)
                    Email.send_email(reciever_email, template['subject'], html)

                elif template_type == 'sms':
                    if reciever:
                        notification = Notification(
                            user_id = reciever.id,
                            user_role = reciever.role,
                            target = reciever_phone,
                            notification_type = template_type,
                            message = message,
                            status = 'pending'
                        )

                        save_db(notification)

                    Fast2SMS.send_sms(reciever_phone, message)

                else:
                    raise Exception("Invalid Notification Type")

        except Exception as e:
            logging.info(f"Error sending notification: {e}")
            return apiresponse(False, "Error sending notification")

class Validation:
    @staticmethod
    def validate_email(email: str):
        try:
            address = email.split("@")[0]
            domain = email.split("@")[1]
            service = domain.split(".")[0]
            suffix = domain.split(".")[1]
            return True
        except Exception:
            return False

    @staticmethod       
    def validate_phone(phone: str):
        try:
            if len(phone) == 10:
                try:
                    phone = int(phone)
                    return True
                except:
                    return False
            else:
                return False
        except Exception:
            return False