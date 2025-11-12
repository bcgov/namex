import os

import flask
import flask_admin
from cloud_sql_connector import DBConfig, setup_search_path_event_listener
from sqlalchemy.orm import scoped_session, sessionmaker
from structured_logging import StructuredLogging

import config
from solr_admin import models
from solr_admin.models import (decision_reason, decision_reason_audit,
                               restricted_condition_audit, synonym,
                               synonym_audit, virtual_word_condition,
                               word_classification)
from solr_admin.oidc_callback import bp as oidc_callback_bp
from solr_admin.views import (decision_reason_audit_view, decision_reason_view,
                              restricted_word_condition_audit_view,
                              synonym_audit_view, synonym_view,
                              virtual_word_condition_view,
                              word_classification_view)


# Create admin site
def create_application(run_mode=os.getenv('FLASK_ENV', 'production')):
    # Create application
    application = flask.Flask(__name__)
    application.config.from_object(config.CONFIGURATION[run_mode])

    schema = application.config.get('DB_SCHEMA', 'public')
    if application.config.get('DB_INSTANCE_CONNECTION_NAME'):
        db_config = DBConfig(
            instance_name=application.config.get('DB_INSTANCE_CONNECTION_NAME'),
            database=application.config.get('DATABASE_NAME'),
            user=application.config.get('DATABASE_USER'),
            ip_type=application.config.get('DB_IP_TYPE'),
            schema=schema,
            pool_recycle=300,
        )
        application.config['SQLALCHEMY_ENGINE_OPTIONS'] = db_config.get_engine_options()

    # Configure Structured Logging
    structured_logger = StructuredLogging()
    structured_logger.init_app(application)
    application.logger = structured_logger.get_logger()

    # Register OIDC callback route to handle Keycloak redirect after login
    application.register_blueprint(oidc_callback_bp)

    models.db.init_app(application)

    with application.app_context():
        schema = application.config.get("DB_SCHEMA", "public")

        if application.config.get("SQLALCHEMY_ENGINE_OPTIONS"):
            engine = models.db.engine
            models.db.session = scoped_session(sessionmaker(bind=engine))
            setup_search_path_event_listener(engine, schema)


    with application.app_context():
        engine = models.db.engine
        setup_search_path_event_listener(engine, schema)

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
