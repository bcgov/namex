
import os

from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

import config
import solr_admin.models
from solr_admin.keycloak import Keycloak
from solr_admin.models.synonym import Synonym
from solr_admin.views.synonym_view import SynonymView


# Create admin
def create_application(run_mode=os.getenv("FLASK_ENV", "production")):
    # Create application
    application = Flask(__name__)
    application.config.from_object(config.CONFIGURATION[run_mode])

    # Do the first call that sets up OIDC for the application.
    Keycloak(application)

    # Create the connection to the database.
    models.db = SQLAlchemy(application)

    # The root page - point the users to the admin interface.
    @application.route("/")
    def index():
        return "<a href=\"/admin/synonym/\"/>Click me to get to Synonyms!</a>"

    flask_admin = Admin(application, name="Solr Configuration", template_mode="bootstrap3")
    flask_admin.add_view(SynonymView(Synonym, models.db.session))

    return application
