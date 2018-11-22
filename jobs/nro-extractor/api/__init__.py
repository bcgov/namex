from api.utils.logging import setup_logging
setup_logging() ## important to do this first

from flask import Flask, g, current_app
from flask_marshmallow import Marshmallow
from config import Config

from namex import db

ma = Marshmallow()

from .endpoints import api


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    api.init_app(app)

    db.init_app(app)
    ma.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        ''' Enable Flask to automatically remove database sessions at the
         end of the request or when the application shuts down.
         Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
        '''
        if hasattr(g, 'db_nro_session'):
            g.db_nro_session.close()

    return app
