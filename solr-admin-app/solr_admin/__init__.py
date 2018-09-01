
import os

import flask
import flask_admin
import flask_sqlalchemy

import config
from solr_admin import keycloak
from solr_admin import models
from solr_admin.models import synonym
from solr_admin.models import synonym_audit
from solr_admin.views import synonym_audit_view
from solr_admin.views import synonym_view


# Create admin
def create_application(run_mode=os.getenv('FLASK_ENV', 'production')):
    # Create application
    application = flask.Flask(__name__)
    application.config.from_object(config.CONFIGURATION[run_mode])

    # Do the call that sets up OIDC for the application.
    keycloak.Keycloak(application)

    # Create the connection to the database.
    models.db = flask_sqlalchemy.SQLAlchemy(application)

    # The root page - point the users to the admin interface.
    @application.route('/')
    def index():
        return '<a href="/admin/synonym/"/>Click me to get to Synonyms!</a>'

    admin = flask_admin.Admin(application, name='Solr Configuration', template_mode='bootstrap3')
    admin.add_view(synonym_view.SynonymView(synonym.Synonym, models.db.session))
    admin.add_view(synonym_audit_view.SynonymAuditView(synonym_audit.SynonymAudit, models.db.session))

    return application
