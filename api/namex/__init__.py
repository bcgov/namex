# -*- coding: utf-8 -*-
"""NAMEX API

This module is the API for the Names Examination system

TODO: Fill in a larger description once the API is defined for V1
"""
from namex.utils.logging import setup_logging
setup_logging() ## important to do this first

import os

from flask import Flask
import config
from flask_jwt_oidc import JwtManager
jwt = JwtManager()

from namex.models import db, ma
from namex.resources import api
from namex import models


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):

    app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])

    db.init_app(app)
    ma.init_app(app)

    api.init_app(app)
    # oidc.init_app(app)
    setup_jwt_manager(app, jwt)

    register_shellcontext(app)

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
            'db': db,
            'models': models}

    app.shell_context_processor(shell_context)