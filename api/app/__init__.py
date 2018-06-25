# -*- coding: utf-8 -*-
"""NAMEX API

This module is the API for the Names Examination system

TODO: Fill in a larger description once the API is defined for V1
"""
import logging
from flask import Flask, current_app
from flask_restplus import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from config import Config
from app.patches.flask_oidc_patched import OpenIDConnect
import os
# from app.models import db
from logging import config

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

db = SQLAlchemy()

application = Flask(__name__, instance_relative_config=True)
application.config.from_object(Config)
db.init_app(application)
ma = Marshmallow(application)

api = Api(application, prefix='/api/v1')

oidc = OpenIDConnect(application)

# noinspection PyPep8
from app.resources.requests import Request
import app.resources.ops

if __name__ == "__main__":
    application.run()
