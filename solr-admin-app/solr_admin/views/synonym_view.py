
import re

from flask import current_app, request
from flask_admin.contrib import sqla
from wtforms import validators

from solr_admin import keycloak
from solr_admin import models
from solr_admin import solr
from solr_admin.models import synonym_audit


# The customized ModelView that is used for working with the synonyms.
class SynonymView(sqla.ModelView):
    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ['delete']

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'synonyms_text'

    # For some reason this needs to be initialized, but we will override it in is_accessible.
    column_editable_list = ['category', 'comment', 'synonyms_text']

    # Allow the user to filter on the category column.
    column_filters = ['category']

    # Search within the synonyms_text.
    column_searchable_list = ['category', 'synonyms_text']

    # Use a custom create.html that warns the user about sorting what they enter.
    create_template = 'synonyms_create.html'

    # Use a custom edit.html that warns the user about sorting what they enter.
    edit_template = 'synonyms_edit.html'

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'synonyms_list.html'

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
            self.column_editable_list = ['category', 'comment', 'synonyms_text']
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
        model.synonyms_text = _alphabetize_csv(model.synonyms_text)
        _validate_synonyms_text(model.synonyms_text)

    # After saving the data create the audit log (we need to wait for a synonym.id value when creating)
    def after_model_change(self, form, model, is_created):
        if is_created:
            _create_audit_log(model, 'CREATE')
        else:
            _create_audit_log(model, 'UPDATE')

        solr.reload_solr_cores()

    # After deleting the data create the audit log.
    def after_model_delete(self, model):
        _create_audit_log(model, 'DELETE')
        solr.reload_solr_cores()


# Validate the Synonyms Text and ensure it meets our standards.
def _validate_synonyms_text(synonyms_text: str) -> None:
    # Split into comma-separated words.
    values = synonyms_text.split(',')

    # Strip leading and trailing spaces.
    values = list(map(str.strip, values))

    _validation_character_check(values)
    _validation_multiple_spaces(values)
    _validation_duplicates_check(values)
    _validation_minimum_count(values)


# Only a-z, 0-9, and space are allowed in the synonyms.
def _validation_character_check(values) -> None:
    disallowed_values = []
    for value in values:
        if re.search('[^a-z0-9 ]', value):
            disallowed_values.append(value)

    if disallowed_values:
        raise validators.ValidationError(
            'Synonyms Text only allows lower case letters, digits, and space characters ({})'
            .format(', '.join(disallowed_values)))


# Multiple spaces are not allowed.
def _validation_multiple_spaces(values) -> None:
    multiple_spaces = []
    for value in values:
        if '  ' in value:
            multiple_spaces.append(value)

    if multiple_spaces:
        raise validators.ValidationError(
            'Synonyms Text does not allow multiple embedded spaces ({})'.format(', '.join(multiple_spaces)))


# Duplicate values are not allowed.
def _validation_duplicates_check(values) -> None:
    duplicate_values = []
    previous_value = ''
    for value in values:
        if value == previous_value:
            duplicate_values.append(value)

        previous_value = value

    if duplicate_values:
        # Remove duplicates, in the case of have triples or more.
        duplicate_values = list(set(duplicate_values))
        duplicate_values.sort()

        raise validators.ValidationError(
            'Synonyms Text does not allow duplicate values ({})'.format(', '.join(duplicate_values)))


# Ensure that there is more than one value.
def _validation_minimum_count(values) -> None:
    if len(values) == 1:
        raise validators.ValidationError('Synonyms Text must contain more than one value')


# Put a CSV string into alphabetical order, and format nicely.
def _alphabetize_csv(string: str) -> str:
    # Split into comma-separated words.
    values = string.split(',')

    # Strip leading and trailing spaces.
    values = list(map(str.strip, values))

    # Remove empty strings.
    values = list(filter(None, values))

    # Sort alphabetically.
    values.sort()

    return ', '.join(values)


# Do the audit logging - we will write the complete record, not the delta (although the latter is possible).
def _create_audit_log(model, action) -> None:
    audit = synonym_audit.SynonymAudit(
        model.id, keycloak.Keycloak(None).get_username(), action, model.category, model.synonyms_text, model.comment,
        model.enabled)

    session = models.db.session
    session.add(audit)
    session.commit()
