# -*- coding: utf-8 -*-
"""NAMEX API.

This module is the API for the Names Examination system

TODO: Fill in a larger description once the API is defined for V1
"""

import config
import os
import structlog

from flask import Flask, request
from flask_jwt_oidc import JwtManager

from .VERSION import __version__

jwt = JwtManager()

from flask_cors import CORS
from flask_migrate import Migrate
from structured_logging import StructuredLogging

from namex.services.cache import cache
from namex.services.lookup import nr_filing_actions
from .services import queue

from namex import models
from namex.models import db, ma
from namex.resources import api
from namex.utils.run_version import get_run_version
from namex.services import flags


run_version = get_run_version()


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):  # noqa: B008
    """Create app."""
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.CONFIGURATION[run_mode])

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    # Add support for request-specific log fields like 'app_name'
    structlog.configure(
        processors=[structlog.contextvars.merge_contextvars] + structlog.get_config()['processors']
    )

    # Bind app-name from request headers into the logging context
    @app.before_request
    def bind_app_name():
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(app_name=request.headers.get('App-Name', 'unknown'))

    flags.init_app(app)
    queue.init_app(app)

    db.init_app(app)
    Migrate(app, db)

    ma.init_app(app)

    api.init_app(app)
    setup_jwt_manager(app, jwt)

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
        return {'app': app, 'jwt': jwt, 'db': db, 'models': models}

    app.shell_context_processor(shell_context)
