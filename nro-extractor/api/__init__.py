from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

from config import Config

import os
import logging.config


db = SQLAlchemy()
ma = Marshmallow()

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

from .endpoints import api

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)

    db.init_app(app)
    ma.init_app(app)

    return app

