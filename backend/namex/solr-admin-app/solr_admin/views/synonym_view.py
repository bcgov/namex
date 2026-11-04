
import re

from wtforms import validators, StringField
from wtforms.validators import DataRequired

from solr_admin import keycloak
from solr_admin import models
from solr_admin import solr
from solr_admin.models import synonym_audit


# The customized ModelView that is used for working with the synonyms.
from solr_admin.services.get_stems import get_stems
from solr_admin.services.get_multi_word_synonyms import get_multi_word_synonyms
from solr_admin.views.secured_view import SecuredView


class SynonymView(SecuredView):
    # We're unlikely to do multiple deletes, so just get rid of the checkboxes and the drop down for delete.
    action_disallowed_list = ['delete']

    # list of model columns
    column_list = ('category', 'synonyms_text', 'stems_text', 'comment', 'enabled')

    # Allow export as a CSV file.
    can_export = True

    # Allow the user to change the page size.
    can_set_page_size = True

    # Keep everything sorted, although realistically also we need to sort the values within a row before it is saved.
    column_default_sort = 'synonyms_text'

    # For some reason this needs to be initialized, but we will override it in is_accessible.
    column_editable_list = ['category', 'comment']

    # Explicitly define synonyms_text field to prevent WTForms from breaking on unique=True, nullable=False
    form_extra_fields = {'synonyms_text': StringField('Synonyms Text', validators=[DataRequired()])}

    # List of visible columns
    form_columns = ['category', 'synonyms_text', 'comment']

    # Allow the user to filter on the category column.
    column_filters = ['category', 'synonyms_text', 'comment' ]

    # Search within the synonyms_text.
    column_searchable_list = ['category', 'synonyms_text', 'comment']

    # Use a custom create.html that warns the user about sorting what they enter.
    create_template = 'synonyms_create.html'

    # Use a custom edit.html that warns the user about sorting what they enter.
    edit_template = 'synonyms_edit.html'

    # Use a custom list.html that provides a page size drop down with extra choices.
    list_template = 'synonyms_list.html'

    # When the user goes to save the data, trim whitespace and put the list back into alphabetical order.
    def on_model_change(self, form, model, is_created):
        model.synonyms_text = _alphabetize_csv(model.synonyms_text)
        _validate_synonyms_text(model.synonyms_text)
        model.stems_text = get_stems(model.synonyms_text)


    # After saving the data create the audit log (we need to wait for a synonym.id value when creating)
    def after_model_change(self, form, model, is_created):
        if is_created:
            _create_audit_log(model, 'CREATE')
        else:
            _create_audit_log(model, 'UPDATE')

        self.session.commit()
        #solr.reload_solr_cores()

    # After deleting the data create the audit log.
    def after_model_delete(self, model):
        _create_audit_log(model, 'DELETE')
        #solr.reload_solr_cores()


# Validate the Synonyms Text and ensure it meets our standards.
def _validate_synonyms_text(synonyms_text: str) -> None:
    # Split into comma-separated words.
    values = synonyms_text.split(',')

    # Strip leading and trailing spaces.
    values = list(map(str.strip, values))

    _validation_multi_word_check(values)
    _validation_character_check(values)
    _validation_multiple_spaces(values)
    _validation_duplicates_check(values)
    _validation_minimum_count(values)

# Check for multi-word synonyms
def _validation_multi_word_check(values) -> None:
    disallowed_values = get_multi_word_synonyms(values)

    if disallowed_values:
        raise validators.ValidationError(
            'Multi-word synonyms text cannot be processed here, please contact application support. ({})'
                .format(', '.join(disallowed_values)))


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
        keycloak.Keycloak().get_username(), action, model.id, model.category, model.synonyms_text, model.comment,
        model.enabled)

    session = models.db.session
    session.add(audit)
    session.commit()
