# -*- coding: utf-8 -*-
"""NAMEX API.

This module is the API for the Names Examination system

TODO: Fill in a larger description once the API is defined for V1
"""
import config
from namex.utils.logging import setup_logging
setup_logging()  # important to do this first

import os

from .VERSION import __version__  # noqa: F401; imported from here
from flask import Flask
from flask_jwt_oidc import JwtManager

jwt = JwtManager()

import sentry_sdk  # noqa: I001; pylint: disable=ungrouped-imports,wrong-import-order; conflicts with Flake8
from sentry_sdk.integrations.flask import FlaskIntegration  # noqa: I001

from namex.services.lookup import nr_filing_actions
from namex.services.nro import NROServices
from namex.services.cache import cache
from .services import queue
nro = NROServices()
from namex.models import db, ma
from namex.resources import api
from namex import models
from namex.utils.run_version import get_run_version
# noqa: I003; dont know what flake8 wants here

run_version = get_run_version()


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Create app."""
    app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])

    # Configure Sentry
    if str(app.config.get('SENTRY_ENABLE')).lower() == 'true':
        if app.config.get('SENTRY_DSN', None):
            sentry_sdk.init(
               dsn=app.config.get('SENTRY_DSN'),
               integrations=[FlaskIntegration()]
            )

    queue.init_app(app)

    db.init_app(app)
    ma.init_app(app)

    api.init_app(app)
    setup_jwt_manager(app, jwt)

    nro.init_app(app)
    cache.init_app(app)
    nr_filing_actions.init_app(app)

    @app.after_request
    def add_version(response):
        os.getenv('OPENSHIFT_BUILD_COMMIT', '')
        response.headers['API'] = 'NameX/{ver}'.format(ver=run_version)
        return response

    register_shellcontext(app)

    return app


def setup_jwt_manager(app, jwt):
    """Initialize jwt config."""
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
