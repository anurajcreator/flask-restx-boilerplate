from app.main.util.v1.encryption import Encryption
from .. import db, flask_bcrypt
import datetime
import jwt
from app.main.model.blacklist import BlacklistToken
from ..config import key

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255),  nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    enc_private_1 = db.Column(db.Unicode)
    private_1_skey = db.Column(db.Unicode)
    private_1_nonce = db.Column(db.Unicode)
    private_1_tag = db.Column(db.Unicode)



    #Static Properties
    @property
    def role(self):
        return 'user'

    #Hashed Properties
    @property
    def password(self):
        raise AttributeError('password: write-only field')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User '{}'>".format(self.username)


    #Encrypted Properties
    @property
    def private_1(self):
        return Encryption.decrypt_data(self.enc_private_1, self.private_1_skey, self.private_1_nonce, self.private_1_tag)

    @private_1.setter
    def private_1(self, private_1):
        self.private_1_skey, self.enc_private_1, self.private_1_nonce, self.private_1_tag = Encryption.encrypt_data(private_1)

    

    def encode_auth_token(self):
        """
        Generates the Auth token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'id': self.id,
                'role': self.role
            }
            auth_token = jwt.encode(payload,key,algorithm='HS256')
            return auth_token
        except Exception as e:
            return e
    