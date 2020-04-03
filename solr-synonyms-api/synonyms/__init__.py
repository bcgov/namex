import os

import flask

import config
import synonyms.endpoints
import synonyms.models


__all__ = ['create_application']

from .VERSION import __version__
from synonyms.utils.run_version import get_run_version
from flask_jwt_oidc import JwtManager

jwtManager = JwtManager()

from synonyms.endpoints import api
from synonyms.models import db, ma

run_version = get_run_version()


def create_application(run_mode=os.getenv('FLASK_ENV', 'production')):
    # Create application
    application = flask.Flask(__name__)
    application.config.from_object(config.CONFIGURATION[run_mode])

    # Create the connection to the database.
    db.init_app(application)
    ma.init_app(application)

    # Initialize the API endpoints.
    api.init_app(application)
    setup_jwt_manager(application, jwtManager)


    @application.after_request
    def add_version(response):
        os.getenv('OPENSHIFT_BUILD_COMMIT', '')
        response.headers["API"] = 'NameX/{ver}'.format(ver=run_version)
        return response

    register_shellcontext(application)

    return application


def setup_jwt_manager(app, token_manager):
    def get_roles(a_dict):
        return a_dict['realm_access']['roles']

    app.config['JWT_ROLE_CALLBACK'] = get_roles

    token_manager.init_app(app)

    return


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'app': app,
            'jwt': jwtManager,
            'db': db,
            'models': models}

    app.shell_context_processor(shell_context)
