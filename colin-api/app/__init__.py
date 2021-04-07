"""NAMEX display corporation details API
"""
import os

from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from flask_jwt_oidc import JwtManager
from app.utils.logging import setup_logging

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first

db = SQLAlchemy()

api = Api(prefix='/api/v1')  # figure out prefix
# db.init_app(application)
ma = Marshmallow()
jwt = JwtManager()
app = None

from app.resources.corporations import RequestColin
import app.resources.ops

def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    api.init_app(app)

    db.init_app(app)
    ma.init_app(app)
    setup_jwt_manager(app,jwt)

    return app

def setup_jwt_manager(app, jwt):
    def get_roles(a_dict):
        return a_dict['realm_access']['roles']

    app.config['JWT_ROLE_CALLBACK'] = get_roles

    jwt.init_app(app)

    return

def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'app': app,
            'jwt': jwt,
            'db': db,}

    app.shell_context_processor(shell_context)
