from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
from .config import config_by_name, photos
from flask_mail import Mail
from flask_cors import CORS
from flask_mongoengine import MongoEngine

db = SQLAlchemy()
flask_bcrypt = Bcrypt()
mail=Mail()
mdb = MongoEngine()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    mdb.init_app(app)
    configure_uploads(app, photos)
    flask_bcrypt.init_app(app)
    mail.init_app(app)
    CORS(app)

    return app

