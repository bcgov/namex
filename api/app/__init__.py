# -*- coding: utf-8 -*-
"""NAMEX API

This module is the API for the Names Examination system

TODO: Fill in a larger description once the API is defined for V1
"""
from app.utils.logging import setup_logging
setup_logging() ## important to do this first

import os

from flask import Flask
from config import Config, configuration
from app.patches.flask_oidc_patched import OpenIDConnect
oidc = OpenIDConnect()

from app.models import db, ma
from app.resources import api
from app import models


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):

    app = Flask(__name__)
    app.config.from_object(configuration[run_mode])

    db.init_app(app)
    ma.init_app(app)

    api.init_app(app)
    oidc.init_app(app)

    register_shellcontext(app)

    return app


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'app': app,
            'db': db,
            'models': models}

    app.shell_context_processor(shell_context)
