from flask import Flask, g, current_app
from config import Config
from namex import db


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)
    app.app_context().push()
    current_app.logger.debug('created the Flask App and pushed the App Context')

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        ''' Enable Flask to automatically remove database sessions at the
         end of the request or when the application shuts down.
         Ref: http://flask.pocoo.org/docs/patterns/sqlalchemy/
        '''
        current_app.logger.debug('Tearing down the Flask App and the App Context')
        if hasattr(g, 'ora_conn'):
            g.ora_conn.close()

    return app
