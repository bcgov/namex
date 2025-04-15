"""SYNONYMS API.

This module is the API for the Names Examination system.
"""
import os

import flask
from flask_jwt_oidc import JwtManager

import config
from synonyms import models
from synonyms.endpoints import api
from synonyms.models import db, ma
from synonyms.utils.run_version import get_run_version
from structured_logging import StructuredLogging

jwt = JwtManager()
run_version = get_run_version()


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Create app."""
    app = flask.Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    db.init_app(app)
    ma.init_app(app)

    api.init_app(app)
    setup_jwt_manager(app, jwt)

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
