from .response_objects.setup import Setup
from string import Template
from .utils import join_list_words


class HelpfulHintSetup(Setup):
    pass


def helpful_hint_setup():
    return HelpfulHintSetup(
        type='helpful_hint', header=Template(''), line1=Template('Helpful Hint'), line2=Template('')
    )


class AddDistinctiveSetup(Setup):
    pass


def add_distinctive_setup():
    return AddDistinctiveSetup(
        type='add_distinctive',
        header=Template('Add Words'),
        line1=Template(
            "Add some words to the beginning of your name that set your name apart. For example: an individual's name or initials, a geographic location, a colour, a coined, made-up word, or an acronym."
        ),
        line2=Template("Example: Change &quot;Renovations Ltd.&quot; to &quot;Joe's Renovations Ltd."),
    )


class AddDescriptiveSetup(Setup):
    pass


def add_descriptive_setup():
    return AddDescriptiveSetup(
        type='add_descriptive',
        header=Template('Add Words'),
        line1=Template(
            'Add some additional words that help describe what your business does. For example, the product or service you provide.'
        ),
        line2=Template("Example: Change &quot;Joe's Ltd.&quot; to &quot;Joe's Renovations Ltd."),
    )


class TooManyWordsSetup(Setup):
    pass


def too_many_words_setup():
    return TooManyWordsSetup(
        type='too_many_words',
        header=Template('Too Many Words'),
        line1=Template(
            'Please remove one or more words and try your search again, or you can choose to submit the name above for examination.'
        ),
        line2=Template(
            "Note: Designations at the end of your name such as 'Limited', 'Inc', 'Cooperative' will not be counted."
        ),
    )


class RemoveSetup(Setup):
    pass


def remove_setup():
    return RemoveSetup(
        type='remove',
        header=Template('Remove or Replace Word(s)'),
        line1=Template('Remove or replace the highlighted words and try your search again.'),
        line2=Template(''),
    )


class RemoveOrReplaceSetup(Setup):
    pass


def remove_or_replace_setup():
    return RemoveOrReplaceSetup(
        type='remove_or_replace',
        header=Template('Remove or Replace Word(s)'),
        line1=Template('Remove or replace the highlighted words and try your search again.'),
        line2=Template(''),
    )


class RemoveOrSubmitSetup(Setup):
    pass


def remove_or_submit_setup():
    return RemoveOrReplaceSetup(
        type='remove_or_submit',
        header=Template('Remove or Submit'),
        line1=Template(
            'Please remove or replace the highlighted words and try your search again, or you can choose to submit the name above for examination.'
        ),
        line2=Template(''),
    )


class ResolveConflictSetup(Setup):
    pass


def resolve_conflict_setup():
    return ResolveConflictSetup(
        type='resolve_conflict',
        header=Template('Add Words'),
        line1=Template(
            'Add a word to the beginning of the name that sets it apart (like a person’s name or initials) '
            'or change some of the words in the name.'
        ),
        line2=Template(''),
    )


class AssumedNameSetup(Setup):
    pass


def assumed_name_setup():
    return AssumedNameSetup(
        type='assumed_name',
        header=Template('Assume a Name'),
        line1=Template(
            'If the name of an extraprovincial business is too similar to an existing BC business, you must use (assume) a different name in BC. Assumed names must be reviewed Registries staff.'
        ),
        action=Template('I want to assume a name in BC'),
        # checkbox=Template("I want to send my name to be examined as an Assumed Name.")
    )


class AlternativeAssumedNameSetup(Setup):
    pass


def alternative_assumed_name_setup():
    return AlternativeAssumedNameSetup(
        type='assumed_name',
        header=Template('Change Business Name'),
        line1=Template(
            'The name of your business must be the same in BC and your home jurisdiction. Change your business name in your home jurisdiction and obtain the same name in BC.'
        ),
        line2=Template('Before obtaining a new name, check to see if the name is available in both jurisdictions.'),
    )


class SendToExaminerSetup(Setup):
    pass


def send_to_examiner_setup():
    return SendToExaminerSetup(
        type='send_to_examiner',
        header=Template('Send for Review'),
        line1=Template(
            'You can choose to submit this name for review without changes. Please check wait times at the top of the screen.'
        ),
        line2=Template(''),
        action=Template('I want to send my name for review'),
    )


class ObtainConsentSetup(Setup):
    pass


def obtain_consent_setup():
    return ObtainConsentSetup(
        type='obtain_consent',
        header=Template('Obtain Consent'),
        line1=Template(
            'This name may be approved if you are able to get written consent <b>from the appropriate authority.</b>'
        ),
        line2=Template(''),
        action=Template('I will submit written consent to the BC Business Registry'),
    )


class SelfConsentSetup(Setup):
    pass


def conflict_self_consent_setup():
    return SelfConsentSetup(
        type='conflict_self_consent',
        header=Template('Obtain Consent'),
        line1=Template(
            'This name may be approved if you are able to get written consent <b>from the registered owner of the conflicting name.</b>'
        ),
        line2=Template(''),
        action=Template('I will submit written consent to the BC Business Registry'),
    )


class ReplaceDesignationSetup(Setup):
    pass


def replace_designation_setup():
    return ReplaceDesignationSetup(
        type='replace_designation',
        header=Template('Change Designation'),
        line1=Template('Change the designation from to one of the following:'),
        line2=Template(''),
    )


class RemoveDesignationSetup(Setup):
    pass


def remove_designation_setup(all_designations_user):
    return ReplaceDesignationSetup(
        type='remove_designation',
        header=Template('Remove Designation'),
        line1=Template(
            'Remove the designation(s) from your name: '
            + join_list_words([element.upper() for element in all_designations_user])
        ),
        line2=Template(''),
    )


class AddDesignationSetup(Setup):
    pass


def add_designation_setup():
    return AddDesignationSetup(
        type='add_designation',
        header=Template('Select Designation'),
        line1=Template('Select a designation from the following:'),
        line2=Template(''),
    )


class ChangeDesignationSetup(Setup):
    pass


def change_designation_order_setup():
    return ChangeDesignationSetup(
        type='change designation at the end',
        header=Template('Change Designation Order'),
        line1=Template('Move the designation to the end of the name.'),
        line2=Template(''),
        label=Template('Move Designation'),
    )


class ChangeEntityTypeSetup(Setup):
    pass


def change_entity_type_setup():
    return ChangeEntityTypeSetup(
        type='change_entity_type',
        header=Template('Change Business Type'),
        line1=Template('Restart name search and select a different business type.'),
        line2=Template(''),
        label=Template('Start Search Over'),
    )


class TwoDesignationsSetup(Setup):
    pass


def two_designations_order_setup():
    return TwoDesignationsSetup(
        type='two_designations',
        header=Template('Keep just one designation'),
        line1=Template('Please select one of the designations listed here:'),
        line2=Template(''),
    )
