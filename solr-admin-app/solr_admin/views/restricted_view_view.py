
import re

from flask import current_app, request
from flask_admin.contrib import sqla
from wtforms import validators


from namex_admin import keycloak
from namex_admin import models
from namex_admin.models import synonym_audit

# The customized ModelView that is used for working with the synonyms.
class RestrictedViewView(sqla.ModelView):

    column_list = ['word_phrase', 'cnd_text', 'consent_required', 'consenting_body', 'instructions', 'allow_use', 'word_id', 'cnd_id']

    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    #action_disallowed_list = ['']

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'cnd_id'

    # Allow the user to filter on the these columns.
    column_filters = ['word_phrase', 'cnd_text', 'consenting_body','cnd_id','word_id']

    # Search within the synonyms_text.
    column_searchable_list = ['cnd_text', 'word_phrase','consenting_body','cnd_id','word_id']

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'generic_list.html'

    #form_choices = {'cnd_text': RestrictedWord.cnd_text}
    # At runtime determine whether or not the user has access to functionality of the view. The rule is that data is
    # only editable in the test environment.
    def is_accessible(self):
        # Disallow editing
        self.can_create = False
        self.can_delete = False
        self.can_edit = False

        # Flask-OIDC function that states whether or not the user is logged in and has permissions.
        return keycloak.Keycloak(None).has_access()

    # At runtime determine what to do if the view is not accessible.
    def inaccessible_callback(self, name, **kwargs):
        # Flask-OIDC function that is called if the user is not logged in or does not have permissions.
        return keycloak.Keycloak(None).get_redirect_url(request.url)


