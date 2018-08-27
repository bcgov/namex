
from flask import request
from flask_admin.contrib.sqla import ModelView

from solr_admin.models import db
from solr_admin.keycloak import Keycloak
from solr_admin.models.synonym_audit import SynonymAudit
import solr_admin.solr


# The customized ModelView that is used for working with the synonyms.
class SynonymView(ModelView):
    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ["delete"]

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = "synonyms_text"

    # Make all columns editable. [temporarily except the Boolean field "enabled" - see Flask-Admin problem 1604]
    column_editable_list = ["category", "comment", "synonyms_text"]

    # Allow the user to filter on the category column.
    column_filters = ["category"]

    # Search within the synonyms_text.
    column_searchable_list = ["category", "synonyms_text"]

    # Use a custom create.html that warns the user about sorting what they enter.
    create_template = "synonyms_create.html"

    # Use a custom edit.html that warns the user about sorting what they enter.
    edit_template = "synonyms_edit.html"

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = "synonyms_list.html"

    # Flask-OIDC function that states whether or not the user is logged in and has permissions.
    def is_accessible(self):
        return Keycloak(None).has_access()

    # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
    def inaccessible_callback(self, name, **kwargs):
        return Keycloak(None).get_redirect_url(request.url)

    # When the user goes to save the data, trim whitespace and put the list back into alphabetical order.
    def on_model_change(self, form, model, is_created):
        if model.synonyms_text is not None:
            # Split into comma-separated words.
            synonyms = model.synonyms_text.split(",")

            # Strip leading and trailing spaces.
            synonyms = list(map(str.strip, synonyms))

            # Sort alphabetically within the synonyms.
            synonyms.sort()

            model.synonyms_text = ", ".join(synonyms)

    # After saving the data create the audit log (we need to wait for a synonym.id value when creating)
    def after_model_change(self, form, model, is_created):
        if is_created:
            self._create_audit_log(model, "CREATE")
        else:
            self._create_audit_log(model, "UPDATE")

        self._reload_solr_cores()

    # After deleting the data create the audit log.
    def after_model_delete(self, model):
        self._create_audit_log(model, "DELETE")
        self._reload_solr_cores()

    # Do the audit logging - we will write the complete record, not the delta (although the latter is possible).
    @staticmethod
    def _create_audit_log(model, action):
        audit = SynonymAudit(model.id, Keycloak(None).get_username(), action, model.category, model.synonyms_text,
                             model.comment, model.enabled)
        db.session.add(audit)
        db.session.commit()

    # Reload the solr cores after a change. This will be very chatty when there are a lot of edits happening.
    @staticmethod
    def _reload_solr_cores():
        solr_admin.solr.reload_solr_cores()
