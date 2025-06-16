

from solr_admin import keycloak
from solr_admin import models
from solr_admin.models import restricted_condition_audit
from solr_admin.services.create_records import create_records
from solr_admin.services.update_records import update_records
from solr_admin.views.secured_view import SecuredView


class VirtualWordConditionView(SecuredView):

    column_labels = {
        'cnd_id': 'cnd_id',
        'word_id': 'word_id',
        'rc_consenting_body': 'consenting body',
        'rc_words': 'word phrase',
        'rc_condition_text': 'condition text',
        'rc_instructions': 'instructions',
        'rc_allow_use': 'allow use',
        'rc_consent_required': 'consent required'
    }

    action_disallowed_list = ['delete']

    can_export = True

    can_set_page_size = True

    column_editable_list = ['rc_consenting_body', 'rc_words', 'rc_condition_text', 'rc_instructions']

    column_filters = ['rc_consenting_body', 'rc_words', 'rc_condition_text', 'rc_instructions']

    column_searchable_list = ['rc_consenting_body', 'rc_words', 'rc_condition_text', 'rc_instructions']

    create_template = 'generic_create.html'
    edit_template = 'generic_edit.html'
    list_template = 'generic_list.html'

    def after_model_change(self, form, model, is_created):
        if is_created:
            create_records(model, self.session)
            _create_audit_log(model, 'CREATE')
        else:
            update_records(self.session)
            _create_audit_log(model, 'UPDATE')

    def after_model_delete(self, model):
        update_records(self.session)
        _create_audit_log(model, 'DELETE')

# Do the audit logging - we will write the complete record, not the delta (although the latter is possible).
def _create_audit_log(model, action) -> None:
    audit = restricted_condition_audit.RestrictedConditionAudit(
    keycloak.Keycloak().get_username(), action,
    model.id, model.rc_condition_text, model.rc_words, model.rc_consent_required, model.rc_consenting_body, model.rc_instructions, model.rc_allow_use)

    session = models.db.session
    session.add(audit)
    session.commit()
