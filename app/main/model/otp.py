from app.main import db
import datetime
import flask_bcrypt

class Otp(db.Model):
    __tablename__ = "otp"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # user_id = db.Column(db.Integer, nullable=False)
    # user_role = db.Column(db.String, nullable = False)
    credential = db.Column(db.String, nullable=False)
    credential_type = db.Column(db.String, nullable=False)
    otp_token = db.Column(db.String, nullable=False)
    verified_at = db.Column(db.DateTime ,nullable=False)
    otp_hash = db.Column(db.String, nullable=False)
    otp_type= db.Column(db.String,nullable=False)
    counter = db.Column(db.Integer,default=0,nullable=False) 
    restriction_time = db.Column(db.DateTime, default=datetime.datetime.utcnow(),nullable = True)
    expire_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    updated_at = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow())
    deleted_at = db.Column(db.DateTime, nullable=True)
    
    
    @property
    def otp(self):
        raise AttributeError('otp: write-only field')

    @otp.setter
    def otp(self, otp):
        self.otp_hash = flask_bcrypt.generate_password_hash(otp).decode('utf-8')

    def check_otp(self, otp):
        return flask_bcrypt.check_password_hash(self.otp_hash, otp)