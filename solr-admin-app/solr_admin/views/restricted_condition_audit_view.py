
from flask import request
from flask_admin.contrib import sqla

from solr_admin import keycloak


# The customized ModelView that is used for working with the restricted condition audit.
class RestrictedConditionAuditView(sqla.ModelView):
    # Disallow the creation of audit events.
    can_create = False

    # Disallow the deletion of audit events.
    can_delete = False

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Disallow the editing of audit events.
    can_edit = False

    # Display by timestamp.
    column_default_sort = ('timestamp', True)

    # Allow the user to filter on the cnd_id and cnd_text columns. Order is significant here.
    column_filters = ['cnd_id','cnd_text']

    # Search within the cnd_text and cnd_id.
    column_searchable_list = ['cnd_text','cnd_id']

    # Use the generic list.html that provides a page size drop down with extra choices.
    list_template = 'generic_list.html'

    # Flask-OIDC function that states whether or not the user is logged in and has permissions.
    def is_accessible(self):
        return keycloak.Keycloak(None).has_access()

    # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
    def inaccessible_callback(self, name, **kwargs):
        return keycloak.Keycloak(None).get_redirect_url(request.url)
