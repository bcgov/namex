import structlog
from flask import request
from structured_logging import StructuredLogging


def configure_logging(app):
    """
    Configure structured logging for the Flask app.

    Sets up a Structlog-based logger and attaches request-specific context
    (e.g., App-Name, method, endpoint) to each log entry.
    """
    structured_logger = StructuredLogging()
    structured_logger.init_app(app)
    app.logger = structured_logger.get_logger()

    # Prepend context-binding to the processor chain
    structlog.configure(
        processors=[structlog.contextvars.merge_contextvars] + structlog.get_config()['processors']
    )

    # Add request metadata to the log context
    @app.before_request
    def bind_app_name():
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(
            app_name=request.headers.get('App-Name', 'unknown'),
            method=request.method,
            endpoint=request.path
        )
