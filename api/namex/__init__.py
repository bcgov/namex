# -*- coding: utf-8 -*-
"""NAMEX API.

This module is the API for the Names Examination system

TODO: Fill in a larger description once the API is defined for V1
"""

import os
import traceback

from flask import Flask
from flask_jwt_oidc import JwtManager

import config

from .VERSION import __version__

jwt = JwtManager()

from cloud_sql_connector import DBConfig, setup_search_path_event_listener
from flask_cors import CORS
from flask_migrate import Migrate, upgrade

from namex import models
from namex.models import db, ma
from namex.resources import api
from namex.services import flags, logging_config
from namex.services.cache import cache
from namex.services.lookup import nr_filing_actions
from namex.utils.run_version import get_run_version
from namex.utils.synonyms_api_auth import patch_synonyms_api_requests

from .services import queue

run_version = get_run_version()


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):  # noqa: B008
    """Create app."""
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config.CONFIGURATION[run_mode])

    logging_config.configure_logging(app)

    if app.config.get("DB_INSTANCE_CONNECTION_NAME"):
        db_config = DBConfig(
            instance_name=app.config.get("DB_INSTANCE_CONNECTION_NAME"),
            database=app.config.get("DB_NAME"),
            user=app.config.get("DB_USER"),
            ip_type=app.config.get("DB_IP_TYPE"),
            schema=schema if run_mode != "migration" else None,
            pool_recycle=300,
        )

        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = db_config.get_engine_options()
    db.init_app(app)

    if run_mode != "migration":
        with app.app_context():
            engine = db.engine
            setup_search_path_event_listener(engine, schema)

    if run_mode == "migration":
        Migrate(app, db)
        app.logger.info("Running migration upgrade.")
        with app.app_context():
            execute_migrations(app)
        app.logger.info("Finished migration upgrade.")
        app.logger.info("Note: endpoints will 404 until the DEPLOYMENT_ENV is switched off of migration.")
    else:
        flags.init_app(app)
        queue.init_app(app)
        schema = app.config.get("DB_SCHEMA", "public")
        ma.init_app(app)

        api.init_app(app)
        setup_jwt_manager(app, jwt)

        cache.init_app(app)
        nr_filing_actions.init_app(app)

        # Install request middleware for identity token injecttion for synonyms API requests.
        with app.app_context():
            patch_synonyms_api_requests()

        @app.after_request
        def add_version(response):
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

def execute_migrations(app):
    """Execute the database migrations."""
    try:
        upgrade(directory="migrations", revision="head", sql=False, tag=None)
    except Exception as e:  # NOQA pylint: disable=broad-except
        app.logger.disabled = False
        error_message = f"Error processing migrations: {e}\n{traceback.format_exc()}"
        app.logger.error(error_message)
        raise e