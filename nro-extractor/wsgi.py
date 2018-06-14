from flask import Flask
from api import create_app, db, ma
from werkzeug.contrib.fixers import ProxyFix

application = create_app()

@application.shell_context_processor
def make_shell_context():
    return {'app': application,
            'db': db,
            'ma': ma}

# application.wsgi_app = ProxyFix(application.wsgi_app)


if __name__ == "__main__":
    application.run()
