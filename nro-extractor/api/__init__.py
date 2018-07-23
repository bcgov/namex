from api.utils.logging import setup_logging
setup_logging() ## important to do this first

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

db = SQLAlchemy()
ma = Marshmallow()

from .endpoints import api

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)

    db.init_app(app)
    ma.init_app(app)

    return app

