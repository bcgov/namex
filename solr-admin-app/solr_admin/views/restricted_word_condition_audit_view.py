
# The customized ModelView that is used for working with the restricted condition audit.
from solr_admin.views.secured_view import SecuredView


# The customized ModelView that is used for working with the restricted condition audit.
class RestrictedConditionAuditView(SecuredView):

    column_labels = {
        'cnd_id': 'Condition Id',
        'cnd_text': 'Condition Text',
    }

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
    column_filters = ['username',  'action', 'cnd_id', 'consenting_body', 'words', 'cnd_text', 'instructions']

    # Search within the cnd_text and cnd_id.
    column_searchable_list = ['username',  'action', 'cnd_id', 'consenting_body', 'words', 'cnd_text', 'instructions']

    # Use the generic list.html that provides a page size drop down with extra choices.
    list_template = 'generic_list.html'
