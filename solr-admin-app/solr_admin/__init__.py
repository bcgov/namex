
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin

import config
import solr_admin.models
from solr_admin.models.synonym import Synonym
from solr_admin.views.synonym_view import SynonymView


# Create admin
def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    # Create application
    app = Flask(__name__)
    app.config.from_object(config.CONFIGURATION[run_mode])

    # Create the connection to the database.
    models.db = SQLAlchemy(app)

    # Flask views
    @app.route("/")
    def index():
        return "<a href=\"/admin/synonym\">Click me to get to Synonyms!</a>"

    solr_admin_app = Admin(app, name="Solr Configuration", template_mode="bootstrap3")
    solr_admin_app.add_view(SynonymView(Synonym, models.db.session))

    return app
