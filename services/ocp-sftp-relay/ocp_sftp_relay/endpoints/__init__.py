from flask import Flask
from flask_restx import Api

from .health import health_api
from .sftp_relay import sftp_api


def init_api(app: Flask):
    """Attatches a Flask RestX API to a Flask app."""
    api = Api(
        app,
        title="Openshift SFTP Relay API",
        version="1.0",
        description="A SFTP relay service for the Namex SFTP NUANS job located in GCP.",
        prefix="/api/v1",
    )
    api.add_namespace(health_api, path="/health")
    api.add_namespace(sftp_api, path="/sftp")
