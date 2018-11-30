
import os

import flask
import flask_admin
import flask_sqlalchemy

import config
from solr_admin import keycloak
from solr_admin import models

from solr_admin.models import synonym
from solr_admin.models import restricted_view
from solr_admin.models import restricted_word
from solr_admin.models import restricted_condition
from solr_admin.models import restricted_link_word_condition
from solr_admin.models import decision_reason
from solr_admin.models import synonym_audit
from solr_admin.models import restricted_word_audit
from solr_admin.models import restricted_condition_audit
from solr_admin.models import restricted_link_word_condition_audit
from solr_admin.models import decision_reason_audit

from solr_admin.views import synonym_view
from solr_admin.views import restricted_view_view
from solr_admin.views import restricted_word_view
from solr_admin.views import restricted_condition_view
from solr_admin.views import restricted_link_word_condition_view
from solr_admin.views import decision_reason_view
from solr_admin.views import synonym_audit_view
from solr_admin.views import restricted_word_audit_view
from solr_admin.views import restricted_condition_audit_view
from solr_admin.views import restricted_link_word_condition_audit_view
from solr_admin.views import decision_reason_audit_view

from solr_admin.views import table_view

from solr_admin.models import restricted_condition2
from solr_admin.views import restricted_condition2_view

# Create admin site
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
        return '<a href="/admin/synonym/"/>Login to administration.</a>'

    admin = flask_admin.Admin(application, name='Namex Administration', template_mode='bootstrap3')

    admin.add_view(synonym_view.SynonymView(synonym.Synonym, models.db.session))
    admin.add_view(restricted_view_view.RestrictedViewView(restricted_view.RestrictedView, models.db.session))

    admin.add_view(restricted_condition2_view.RestrictedCondition2View(restricted_condition2.RestrictedCondition2, models.db.session))

    admin.add_view(restricted_word_view.RestrictedWordView(restricted_word.RestrictedWord, models.db.session))
    admin.add_view(restricted_condition_view.RestrictedConditionView(restricted_condition.RestrictedCondition, models.db.session))
    admin.add_view(restricted_link_word_condition_view.RestrictedLinkWordConditionView(restricted_link_word_condition.RestrictedLinkWordCondition, models.db.session))
    admin.add_view(decision_reason_view.DecisionReasonView(decision_reason.DecisionReason, models.db.session))

    admin.add_view(synonym_audit_view.SynonymAuditView(synonym_audit.SynonymAudit, models.db.session))
    admin.add_view(restricted_word_audit_view.RestrictedWordAuditView(restricted_word_audit.RestrictedWordAudit, models.db.session))
    admin.add_view(restricted_condition_audit_view.RestrictedConditionAuditView(restricted_condition_audit.RestrictedConditionAudit, models.db.session))
    admin.add_view(restricted_link_word_condition_audit_view.RestrictedLinkWordConditionAuditView(restricted_link_word_condition_audit.RestrictedLinkWordConditionAudit, models.db.session))
    admin.add_view(decision_reason_audit_view.DecisionReasonAuditView(decision_reason_audit.DecisionReasonAudit, models.db.session))

    #admin.add_view(table_view.TableView(restricted_condition.RestrictedCondition,models.db.session))

    return application
