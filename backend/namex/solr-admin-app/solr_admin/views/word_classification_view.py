
from solr_admin import keycloak
from solr_admin import models


# The customized ModelView that is used for working with the word classification
from solr_admin.views.secured_view import SecuredView


class WordClassificationView(SecuredView):

    column_list = ['classification','word', 'last_name_used', 'last_prep_name', 'frequency',
                   'approved_by', 'approved_dt','start_dt', 'end_dt', 'last_updated_by', 'last_updated_dt']

    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ['delete']

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'word'

    #This needs to be initialized, but we will override it in is_accessible.
    column_editable_list = ['classification','word', 'start_dt', 'end_dt']

    # Allow the user to filter on the these columns.
    column_filters = ['classification','word']

    # Search within the words phrases.
    column_searchable_list = ['classification','word']

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



