
# The customized ModelView that is used for working with the synonym audits.
from solr_admin.views.secured_view import SecuredView


class SynonymAuditView(SecuredView):
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

    # Allow the user to filter on the synonym_id and category columns. Order is significant here.
    column_filters = ['username',  'action', 'synonym_id', 'category', 'synonyms_text', 'comment']

    # Search within the synonyms_text.
    column_searchable_list = ['username',  'action', 'synonym_id', 'category', 'synonyms_text', 'comment']

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'synonyms_list.html'

