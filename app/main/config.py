import os
from dotenv import load_dotenv
import json
from flask_uploads import UploadSet,IMAGES

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv()

#MAIL GUN CONFIG
mailing_domain=os.getenv("MAILING_DOMAIN")
test_server_domain=os.getenv("TESTING_LIST")
user_login=os.getenv("ACCOUNT_ACTIVATION")
MAILGUN_API_KEY = os.getenv("MAILGUN_API_KEY")
ACCOUNT_ACTIVATION_DOMAIN=f"{user_login}@{mailing_domain}"
MAILGUN_MESSAGES_ENDPOINT = os.getenv("MAILGUN_MESSAGES_ENDPOINT")
MAILING_HOST=os.getenv("MAILING_DOMAIN")
domain_name = os.getenv("MAILING_DOMAIN")
#END

#FAST2SMS IMPLEMENTATION
FAST2SMS_URL=os.getenv('FAST2SMS_URL')
FAST2SMS_AUTH_HEADER=os.getenv('FAST2SMS_AUTH_HEADER')
FAST2SMS_SENDER_ID=os.getenv('FAST2SMS_SENDER_ID')
FAST2SMS_ROUTE=os.getenv('FAST2SMS_ROUTE')
#END

#FILE UPLOAD
UPLOAD_FOLDER = 'app/main/files'
UPLOADED_PHOTOS_DEST = 'app/main/files' 
MAX_CONTENT_LENGTH = 5 * 1024 * 1024
STATIC_FOLDER = 'app/main/static/'
photos = UploadSet("photos", IMAGES)
image_name_size = 30
download_dir= basedir.replace("/app/main","") + "/Downloads/"
#END

#DATABASE CONFIG
DATABASE_URL=os.getenv('DATABASE_URL') #Server
SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT')
SECRET_KEY = os.getenv('SECRET_KEY')
#END

#OBJECT STORAGE CONFIG
S3_BUCKET                 = os.environ.get('S3_BUCKET')
S3_KEY                    = os.environ.get('S3_KEY')
S3_SECRET                 = os.environ.get('S3_SECRET')
S3_DEFAULT_REGION         = os.environ.get('S3_DEFAULT_REGION')

bucket_link = f"https://{S3_BUCKET}.s3.{S3_DEFAULT_REGION}.amazonaws.com/"
#END

#PAYU_CONFIG
PAYU_MODE = "TEST"
PAYU_MERCHANT_KEY = os.getenv('PAYU_MERCHANT_KEY')
PAYU_MERCHANT_SALT = os.getenv('PAYU_MERCHANT_SALT')
#END

#Logging Dirs
SERVICE_LOGGING_DIR=os.getenv('SERVICE_LOGGING')
#END

master_pass = os.getenv("MASTER_PASSWORD")
encryption_password = os.getenv("ENCRYPTION_PASSWORD")
initialization_vector = os.getenv("INITIALIZATION_VECTOR")
encryption_status = os.getenv("ENCRYPTION_STATUS")
KEY_PAIR_DIR = os.getenv("KEY_PAIR_DIR")

item_per_page = [5,10,25,50,100]

#BUCKET DIRS
profile_pic_dir = "thb/profile_pic"

with open ('app/main/templates/message_templates.json', 'r+') as myfile:
    notification_templates = json.loads(myfile.read())

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SECURITY_PASSWORD_SALT = SECURITY_PASSWORD_SALT
    UPLOAD_FOLDER=UPLOAD_FOLDER
    STATIC_FOLDER = STATIC_FOLDER
    UPLOADED_PHOTOS_DEST = UPLOADED_PHOTOS_DEST
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True
    PAYU_MERCHANT_KEY = PAYU_MERCHANT_KEY
    PAYU_MERCHANT_SALT = PAYU_MERCHANT_SALT

class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PRESERVE_CONTEXT_ON_EXCEPTION = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'flask_boilerplate_test.db')
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}

def version(path:str,version=1):
    return f'/v{str(version)}/{path}'