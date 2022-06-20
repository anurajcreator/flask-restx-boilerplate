# app/__init__.py

from flask_restx import Api
from flask import Blueprint

from app.main.controller.v1.auth.auth_controller import api as auth_ns
from app.main.controller.v1.user.user_controller import api as user_ns
from app.main.config import PROJECT_DESCRIPTION, PROJECT_TITLE, PROJECT_VERSION, authorizations, version
from app.main.util.v1.decorator import token_required




blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title=PROJECT_TITLE,
          version=PROJECT_VERSION,
          description=PROJECT_DESCRIPTION,
          authorizations=authorizations,
          )

api.add_namespace(auth_ns, path=version('auth'))
api.add_namespace(user_ns, path=version('user'))
# api.add_namespace(path="/")



