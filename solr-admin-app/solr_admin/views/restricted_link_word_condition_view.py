
import re

from flask import current_app, request
from flask_admin.contrib import sqla
from wtforms import validators
from solr_admin.models import restricted_link_word_condition_audit

from solr_admin import keycloak
from solr_admin import models


# The customized ModelView that is used for working with the synonyms.
class RestrictedLinkWordConditionView(sqla.ModelView):

    column_list = ['word_id', 'cnd_id']

    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ['delete']

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'word_id'

    #This needs to be initialized, but we will override it in is_accessible.
    column_editable_list = ['word_id', 'cnd_id']

    # Allow the user to filter on the these columns.
    column_filters = ['word_id','cnd_id']

    # Search within the words phrases.
    column_searchable_list = ['word_id','cnd_id']

    # Use a custom create.html that warns the user about sorting what they enter.
    create_template = 'generic_create.html'

    # Use a custom edit.html that warns the user about sorting what they enter.
    edit_template = 'generic_edit.html'

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'generic_list.html'

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
            # Make all columns editable. [temporarily except the Boolean field "enabled" - see Flask-Admin problem 1604]
            self.column_editable_list = ['word_id','cnd_id']
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
        _validate_id_exist(model.cnd_id)
        _validate_id_exist(model.word_id)

    # After saving the data create the audit log (we need to wait for a synonym.id value when creating)
    def after_model_change(self, form, model, is_created):
        if is_created:
            _create_audit_log(model, 'CREATE')
        else:
            _create_audit_log(model, 'UPDATE')

    # After deleting the data create the audit log.
    def after_model_delete(self, model):
        _create_audit_log(model, 'DELETE')

# Validate the id exists.
def _validate_id_exist(test_id: str) -> None:
    pass

# Do the audit logging - we will write the complete record, not the delta (although the latter is possible).
def _create_audit_log(model, action) -> None:
    audit = restricted_link_word_condition_audit.RestrictedLinkWordConditionAudit(
        keycloak.Keycloak(None).get_username(), action,model.link_id, model.cnd_id, model.word_id)

    session = models.db.session
    session.add(audit)
    session.commit()