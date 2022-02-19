from app.main import db
import datetime

class Notifications(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,nullable=False)
    user_role = db.Column(db.String, nullable=False)
    target = db.Column(db.String, nullable=False)
    notification_type = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    status = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow()),
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    deleted_at = db.Column(db.DateTime, nullable=True)

    
    