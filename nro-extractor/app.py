from flask import Flask
from api import create_app, db, ma
from werkzeug.contrib.fixers import ProxyFix

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {'app': app,
            'db': db,
            'ma': ma}

# app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)


if __name__ == "__main__":
    app.run(debug=True)
