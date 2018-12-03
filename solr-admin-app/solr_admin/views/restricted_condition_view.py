
import re

from flask import current_app, request
from flask_admin.contrib import sqla
from wtforms import validators

from solr_admin import keycloak
from solr_admin import models
from solr_admin.models import restricted_condition_audit

# The customized ModelView that is used for working with the restricted conditions.
class RestrictedCondition2View(sqla.ModelView):

    column_list = ['cnd_id','cnd_text','consent_required','consenting_body','instructions','allow_use','word_phrase']

    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ['delete']

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'cnd_id'

    #This needs to be initialized, but we will override it in is_accessible.
    column_editable_list = ['cnd_text','consent_required','consenting_body','instructions','allow_use','word_phrase']

    # Allow the user to filter on the these columns.
    column_filters = ['cnd_id','consenting_body','cnd_text']

    # Search within the words phrases.
    column_searchable_list = ['cnd_id','consenting_body','cnd_text']

    # Use a custom create.html that warns the user about sorting what they enter.
    create_template = 'generic_create.html'

    # Use a custom edit.html that warns the user about sorting what they enter.
    edit_template = 'generic_edit.html'

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'generic_list.html'

    def get_query(self):
        from solr_admin.models.restricted_condition import RestrictedCondition2
        from solr_admin.models.restricted_word_table import RestrictedWordTable

        return self.session.query(RestrictedCondition2, RestrictedWordTable).\
            filter(RestrictedCondition2.cnd_id==RestrictedWordTable.cnd_id).\
            order_by(RestrictedCondition2.cnd_id, RestrictedWordTable.word_id)

    def get_list(self, page, sort_column, sort_desc, search, filters,
                 execute=True, page_size=None):
        from solr_admin.models.restricted_condition import RestrictedCondition2
        count, query = sqla.ModelView.get_list(self, page, sort_column, sort_desc, search, filters, True, page_size)

        data = list()
        previous_condition = None
        previous_word = None
        for row in query:
            tmp, word = row
            condition = RestrictedCondition2(cnd_id=tmp.cnd_id,
                                             cnd_text=tmp.cnd_text,
                                             allow_use=tmp.allow_use,
                                             consent_required=tmp.consent_required,
                                             consenting_body=tmp.consenting_body,
                                             instructions=tmp.instructions,
                                             word_phrase=word.word)
            if previous_word is None:
                data.append(condition)
            else:
                if word.cnd_id != previous_word.cnd_id:
                    data.append(condition)
                else:
                    previous_condition.word_phrase += ', ' + word.word
            previous_condition = condition
            previous_word = word

        return count, data


    #form_choices = {'cnd_text': RestrictedWord.cnd_text}
    # At runtime determine whether or not the user has access to functionality of the view. The rule is that data is
    # only editable in the test environment.
    def is_accessible(self):
        # Disallow editing unless in the 'testing' environment.
        editable = current_app.env == 'testing'
        self.can_create = editable
        self.can_delete = editable
        self.can_edit = editable

        if editable:
            # Make columns editable.
            self.column_editable_list = ['cnd_text','consent_required','consenting_body','instructions','allow_use','word_phrase']
        else:
            self.column_editable_list = []

        # Flask-OIDC function that states whether or not the user is logged in and has permissions.
        return keycloak.Keycloak(None).has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
        return keycloak.Keycloak(None).get_redirect_url(request.url)

    # When the user goes to save the data, trim whitespace and put the list back into alphabetical order.
    def on_model_change(self, form, model, is_created):
        pass
        # _validate_something??(model.cnd_text)

    # After saving the data create the audit log (we need to wait for a new id value when creating)
    def after_model_change(self, form, model, is_created):
        if is_created:
            _create_audit_log(model, 'CREATE')
        else:
            _create_audit_log(model, 'UPDATE')

    # After deleting the data create the audit log.
    def after_model_delete(self, model):
        _create_audit_log(model, 'DELETE')

# Do the audit logging - we will write the complete record, not the delta (although the latter is possible).
def _create_audit_log(model, action) -> None:
    pass
    #audit = restricted_condition_audit.RestrictedConditionAudit(
    #    keycloak.Keycloak(None).get_username(), action,  model.cnd_id, model.cnd_text, model.consent_required,
    #    model.consenting_body, model.instructions, model.allow_use)

    #session = models.db.session
    #session.add(audit)
    #session.commit()
