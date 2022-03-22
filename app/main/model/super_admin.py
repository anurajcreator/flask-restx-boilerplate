import flask
from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key
from app.main.util.v1.encryption import Encryption

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    enc_email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    enc_username = db.Column(db.String(255), unique=True)
    password_hash = db.Column(db.String(255))


    #Static Properties
    @property
    def role(self):
        return 'super_admin'

    #Hashed Properties
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    
    #Hashed Property Operators
    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password)

    def check_password(self, password):

        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)

    #Encrypted Properties
    @property
    def email(self):
        return Encryption.decrypt_data(self.enc_email)

    @property
    def username(self):
        return Encryption.decrypt_data(self.enc_username)

    @email.setter
    def email(self, email):
        self.enc_email = Encryption.encrypt_data(email)
    
    @username.setter
    def username(self, username):
        self.enc_email = Encryption.encrypt_data(username)

        








    def encode_auth_token(self, user_id):
        """
        Generates the Auth token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            # print(payload)
            auth_token = jwt.encode(payload,key,algorithm='HS256')
            return auth_token
        except Exception as e:
            return e
    
    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token,key,algorithms=['HS256'])
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except  jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

