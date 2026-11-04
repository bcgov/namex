
from solr_admin import keycloak
from solr_admin import models
from solr_admin.models import decision_reason_audit

# The customized ModelView that is used for working with the decision reason.
from solr_admin.views.secured_view import SecuredView


class DecisionReasonView(SecuredView):

    column_list = ['name','reason']

    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ['delete']

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'name'

    #This needs to be initialized, but we will override it in is_accessible.
    column_editable_list = ['name','reason']

    # Allow the user to filter on the these columns.
    column_filters = ['name','reason']

    # Search within the words phrases.
    column_searchable_list = ['name','reason']

    # Use a custom create.html that warns the user about sorting what they enter.
    create_template = 'generic_create.html'

    # Use a custom edit.html that warns the user about sorting what they enter.
    edit_template = 'generic_edit.html'

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'generic_list.html'

    # When the user goes to save the data, trim whitespace and put the list back into alphabetical order.
    def on_model_change(self, form, model, is_created):
        pass
        # _validate_something(model.name)


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
    audit = decision_reason_audit.DecisionReasonAudit(
        keycloak.Keycloak().get_username(), action, model.id, model.name, model.reason)

    session = models.db.session
    session.add(audit)
    session.commit()
