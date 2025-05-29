import os

import flask
import flask_admin
import flask_sqlalchemy
from structured_logging import StructuredLogging

import config
from solr_admin.oidc_callback import bp as oidc_callback_bp
from solr_admin import models

from solr_admin.models import synonym
from solr_admin.models import virtual_word_condition
from solr_admin.models import decision_reason
from solr_admin.models import word_classification

from solr_admin.models import synonym_audit
from solr_admin.models import restricted_condition_audit
from solr_admin.models import decision_reason_audit


from solr_admin.views import synonym_view
from solr_admin.views import virtual_word_condition_view
from solr_admin.views import decision_reason_view
from solr_admin.views import word_classification_view

from solr_admin.views import synonym_audit_view
from solr_admin.views import restricted_word_condition_audit_view
from solr_admin.views import decision_reason_audit_view

# Create admin site
def create_application(run_mode=os.getenv('FLASK_ENV', 'production')):
    # Create application
    application = flask.Flask(__name__)
    application.config.from_object(config.CONFIGURATION[run_mode])

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(application)
    application.logger = structured_logger.get_logger()

    # Register OIDC callback route to handle Keycloak redirect after login
    application.register_blueprint(oidc_callback_bp) 

    # Create the connection to the database.
    models.db = flask_sqlalchemy.SQLAlchemy(application)

    # The root page - point the users to the admin interface.
    @application.route('/')
    def index():
        return '<a href="/admin/synonym/"/>Login to administration.</a>'

    admin = flask_admin.Admin(application, name='Namex Administration', template_mode='bootstrap3')

    admin.add_view(synonym_view.SynonymView(synonym.Synonym, models.db.session))
    admin.add_view(virtual_word_condition_view.VirtualWordConditionView(virtual_word_condition.VirtualWordCondition, models.db.session, name='Restricted Word Condition'))
    admin.add_view(decision_reason_view.DecisionReasonView(decision_reason.DecisionReason, models.db.session))
    admin.add_view(word_classification_view.WordClassificationView(word_classification.WordClassification, models.db.session))

    admin.add_view(synonym_audit_view.SynonymAuditView(synonym_audit.SynonymAudit, models.db.session))
    admin.add_view(restricted_word_condition_audit_view.RestrictedConditionAuditView(restricted_condition_audit.RestrictedConditionAudit, models.db.session))
    admin.add_view(decision_reason_audit_view.DecisionReasonAuditView(decision_reason_audit.DecisionReasonAudit, models.db.session))

    return application, admin
