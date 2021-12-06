import os
import unittest
from app.main import create_app, db
from app.main.model import user
from app.main.model import blacklist
from flask_migrate import Migrate
from app import blueprint

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)
migrate = Migrate(app, db)
app.app_context().push()

application = app