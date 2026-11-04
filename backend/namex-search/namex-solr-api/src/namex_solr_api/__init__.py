# Copyright © 2025 Province of British Columbia
#
# Licensed under the BSD 3 Clause License, (the "License");
# you may not use this file except in compliance with the License.
# The template for the license can be found here
#    https://opensource.org/license/bsd-3-clause/
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software
#    without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS”
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
# THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
"""The namex solr api service.

This module is the API for the NameX Solr system.
"""
import os
from http import HTTPStatus
from uuid import uuid4

from cloud_sql_connector import (
    DBConfig,
    setup_pg8000_close_event_listener,
)
from flask import Flask, current_app, redirect, request
from flask_migrate import Migrate

from flask_jwt_oidc import JwtManager
from namex_solr_api import models
from namex_solr_api.config import DevelopmentConfig, MigrationConfig, ProductionConfig, UnitTestingConfig
from namex_solr_api.models import db
from namex_solr_api.resources import internal_bp, ops_bp, v1_bp
from namex_solr_api.services import jwt, solr
from namex_solr_api.services.auth import auth_cache
from namex_solr_api.services.namex_solr.utils.analysis_helpers import analysis_cache
from namex_solr_api.version import get_run_version
from structured_logging import StructuredLogging

CONFIG_MAP = {
    "development": DevelopmentConfig,
    "testing": UnitTestingConfig,
    "migration": MigrationConfig,
    "production": ProductionConfig
}

def create_app(environment: str = os.getenv("DEPLOYMENT_ENV", "production"), **kwargs):
    """Return a configured Flask App using the Factory method."""
    app = Flask(__name__)
    app.logger = StructuredLogging(app).get_logger().new(worker_id=str(uuid4()))
    app.config.from_object(CONFIG_MAP.get(environment, ProductionConfig))

    if app.config.get("CLOUDSQL_INSTANCE_CONNECTION_NAME"):
        schema = "public"
        db_config = DBConfig(
            instance_name=app.config["CLOUDSQL_INSTANCE_CONNECTION_NAME"],
            database=app.config["DB_NAME"],
            user=app.config["DB_USER"],
            ip_type=app.config["DB_IP_TYPE"],
            schema=schema if environment != "migration" else None,
            pool_timeout=int(app.config["DB_CONN_WAIT_TIMEOUT"]),
            pool_recycle=int(app.config["DB_CONN_TIMEOUT"]),
            pool_size=int(app.config["DB_MIN_POOL_SIZE"]),
            max_overflow=int(app.config["DB_MAX_POOL_SIZE"]) - int(app.config["DB_MIN_POOL_SIZE"]),
        )
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = db_config.get_engine_options()

    db.init_app(app)

    if environment != "migration" and app.config.get("CLOUDSQL_INSTANCE_CONNECTION_NAME"):
        with app.app_context():
            engine = db.engine
            setup_pg8000_close_event_listener(engine)

    if environment == "migration":
        Migrate(app, db)

    else:
        solr.init_app(app)
        app.register_blueprint(internal_bp)
        app.register_blueprint(ops_bp)
        app.register_blueprint(v1_bp)
        setup_jwt_manager(app, jwt)
        auth_cache.init_app(app)
        analysis_cache.init_app(app)

    @app.route("/")
    def be_nice_swagger_redirect():
        return redirect("/api/v1", code=HTTPStatus.MOVED_PERMANENTLY)

    @app.before_request
    def add_logger_context():
        current_app.logger.debug("path: %s, app_name: %s, account_id: %s, api_key: %s",
                                 request.path,
                                 request.headers.get("app-name"),
                                 request.headers.get("account-id"),
                                 request.headers.get("x-apikey"))

    @app.after_request
    def add_version(response):
        version = get_run_version()
        response.headers["API"] = f"namex_solr_api/{version}"
        return response

    register_shellcontext(app)

    return app


def setup_jwt_manager(app: Flask, jwt_manager: JwtManager):
    """Use flask app to configure the JWTManager to work for a particular Realm."""
    def get_roles(a_dict):
        return a_dict["realm_access"]["roles"]
    app.config["JWT_ROLE_CALLBACK"] = get_roles

    jwt_manager.init_app(app)


def register_shellcontext(app: Flask):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            "app": app,
            "jwt": jwt,
            "db": db,
            "models": models}

    app.shell_context_processor(shell_context)

