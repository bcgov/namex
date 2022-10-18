
import os

import flask

from solr_feeder import config
from solr_feeder.endpoints import endpoint


__all__ = ['create_application']


# Create the Flask application
def create_application(run_mode=os.getenv('FLASK_ENV', 'production')):
    # Create application
    application = flask.Flask(__name__)
    application.config.from_object(config.CONFIGURATION[run_mode])
    endpoint.init_app(application)

    return application
