
from flask import request
from flask_admin.contrib.sqla import ModelView

from solr_admin.keycloak import Keycloak


# The customized ModelView that is used for working with the synonyms.
class SynonymView(ModelView):
    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ["delete"]

    # Allow the user to change the page size.
    can_set_page_size = True

    # Allow export as a CSV file.
    can_export = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = "synonyms_text"

    # Search within the synonyms_text.
    column_searchable_list = ["synonyms_text"]

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

            model.synonyms_text = ",".join(synonyms)
