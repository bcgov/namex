"""NAMEX display corporation details API
"""

from flask import Flask
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from app.patches.flask_oidc_patched import OpenIDConnect


db = SQLAlchemy()

api = Api(prefix='/api/v1')  # figure out prefix
# db.init_app(application)
ma = Marshmallow()
oidc = OpenIDConnect()
app = None

from app.resources.corporations import RequestColin
import app.resources.ops

def create_app(config=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)
    api.init_app(app)

    db.init_app(app)
    ma.init_app(app)
    oidc.init_app(app)

    return app