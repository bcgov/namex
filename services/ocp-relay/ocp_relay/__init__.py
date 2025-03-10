from flask import Flask

from config import Config
from ocp_relay.endpoints import init_api
from ocp_relay.services.auth import jwt, setup_jwt_manager
from ocp_relay.services.logging import setup_logging

setup_logging()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_api(app)
    setup_jwt_manager(app)
    register_shellcontext(app)

    return app


def register_shellcontext(app: Flask):
    def shell_context():
        return {
            "app": app,
            "jwt": jwt,
        }

    app.shell_context_processor(shell_context)
