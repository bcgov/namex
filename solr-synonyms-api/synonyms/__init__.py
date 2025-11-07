"""SYNONYMS API.

This module is the API for the Names Examination system.
"""
import os

import flask
from flask import Flask
from flask_jwt_oidc import JwtManager
from structured_logging import StructuredLogging

from config import CONFIGURATION
from synonyms import models
from synonyms.endpoints import api
from synonyms.models import db, ma
from synonyms.utils.run_version import get_run_version

jwt = JwtManager()
run_version = get_run_version()


def create_app(run_mode=None):
    """Create app."""
    if run_mode is None:
        run_mode = os.getenv("FLASK_ENV", "production")

    app = flask.Flask(__name__)

    if isinstance(run_mode, type):
        app.config.from_object(run_mode)
    else:
        app.config.from_object(CONFIGURATION[run_mode])
    
    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    db.init_app(app)

    # Initialize Marshmallow with handling for SQLAlchemy auto-detection issues
    try:
        # Try normal initialization first
        ma.init_app(app)
    except AttributeError as e:
        if 'db' in str(e):
            # If the auto-detection fails, initialize without SQLAlchemy and set it manually
            ma.app = app
            ma._db = db  # Manually set the database reference
            app.extensions['marshmallow'] = ma
        else:
            raise

    api.init_app(app)
    setup_jwt_manager(app, jwt)

    @app.after_request
    def add_version(response):
        response.headers["API"] = f"NameX/{run_version}"
        return response

    register_shellcontext(app)

    return app


def setup_jwt_manager(app, jwt):
    def get_roles(a_dict):
        return a_dict["realm_access"]["roles"]
    app.config["JWT_ROLE_CALLBACK"] = get_roles
    jwt.init_app(app)


def register_shellcontext(app):
    def shell_context():
        return {
            "app": app,
            "jwt": jwt,
            "db": db,
            "models": models,
        }
    app.shell_context_processor(shell_context)