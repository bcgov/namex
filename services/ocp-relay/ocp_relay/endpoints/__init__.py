from flask import Flask
from flask_restx import Api

from .health import health_api
from .payment_invoices import payment_invoices_api
from .sftp_relay import sftp_api


def init_api(app: Flask):
    """Attatches a Flask RestX API to a Flask app."""
    api = Api(
        app,
        title="Openshift Relay API",
        version="1.0",
        description="A GCP --> OCP relay service for the Namex API in GCP to use.",
    )
    api.add_namespace(health_api, path="/health")
    api.add_namespace(sftp_api, path="/sftp")
    api.add_namespace(payment_invoices_api, path="/payments")
