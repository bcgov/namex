from .response_objects.setup import Setup
from string import Template


class HelpfulHintSetup(Setup):
    pass


def helpful_hint_setup():
    return HelpfulHintSetup(
        type="helpful_hint",
        header=Template(""),
        line1=Template("Helpful Hint"),
        line2=Template("")
    )


class AddDistinctiveSetup(Setup):
    pass


def add_distinctive_setup():
    return AddDistinctiveSetup(
        type="add_distinctive",
        header=Template("Add Distinctive"),
        line1=Template("Add some words to the beginning of your name that sets your name apart. For example, an individual's name or initials; a geographic location; a colour; a coined, made-up word; or an acronym."),
        line2=Template("Example: Change 'Renovations Ltd.' → 'Joe's Renovations Ltd.")
    )


class AddDescriptiveSetup(Setup):
    pass


def add_descriptive_setup():
    return AddDistinctiveSetup(
        type="add_descriptive",
        header=Template("Add Descriptive"),
        line1=Template("Add some additional words that help describe what your business does. For example, the product or service you provide."),
        line2=Template("Example: Change 'Joe's Ltd.' → 'Joe's Renovations Ltd.")
    )


class TooManyWordsSetup(Setup):
    pass


def too_many_words_setup():
    return TooManyWordsSetup(
        type="too_many_words",
        header=Template("Too Many Words"),
        line1=Template("Please remove one or more words and try your search again, or you can choose to submit the name above for examination."),
        line2=Template("Note: Designations at the end of your name such as 'Limited', 'Inc', 'Cooperative' will not be counted.")
    )


class RemoveSetup(Setup):
    pass


def remove_setup():
    return RemoveSetup(
        type="remove",
        header=Template("Remove"),
        line1=Template("Please remove or replace the word from your search and try again."),
        line2=Template("")
    )


class RemoveOrReplaceSetup(Setup):
    pass


def remove_or_replace_setup():
    return RemoveOrReplaceSetup(
        type="remove_or_replace",
        header=Template("Remove or Replace"),
        line1=Template("Please remove or replace the highlighted words and try your search again."),
        line2=Template("")
    )


class RemoveOrSubmitSetup(Setup):
    pass


def remove_or_submit_setup():
    return RemoveOrReplaceSetup(
        type="remove_or_submit",
        header=Template("Remove or Submit"),
        line1=Template("Please remove or replace the highlighted words and try your search again, or you can choose to submit the name above for examination."),
        line2=Template("")
    )


class ResolveConflictSetup(Setup):
    pass


def resolve_conflict_setup():
    return ResolveConflictSetup(
        type="resolve_conflict",
        header=Template("Resolve Conflict"),
        line1=Template("Add a word to the beginning of the name that sets it apart like a person’s name or initials."),
        line2=Template("Or remove the word(s) $list_remove and replace them with different ones.")
    )


class SendToExaminerSetup(Setup):
    pass


def send_to_examiner_setup():
    return SendToExaminerSetup(
        type="send_to_examiner",
        header=Template("Send to Examiner"),
        line1=Template("You can choose to submit this name for examination. Please check wait times at the top of the screen."),
        line2=Template(""),
        action=Template("I want my name examined.")
    )


class ObtainConsentSetup(Setup):
    pass


def obtain_consent_setup():
    return ObtainConsentSetup(
        type="obtain_consent",
        header=Template("Obtain Consent"),
        line1=Template("This name can be approved, but you will be required to send written consent to the BC Business Registry."),
        line2=Template(""),
        action=Template("I am able to obtain and send written consent.")
    )


class SelfConsentSetup(Setup):
    pass


def conflict_self_consent_setup():
    return SelfConsentSetup(
        type="conflict_self_consent",
        header=Template("Conflict Self Consent"),
        line1=Template("This name can be approved if you are the registered owner of the conflicting name, but you are required to send written consent to the BC Business Registry."),
        line2=Template(""),
        action=Template("I am the registered owner of the conflicting name. I will send written consent.")
    )


class ReplaceDesignationSetup(Setup):
    pass


def replace_designation_setup():
    return ReplaceDesignationSetup(
        type="replace_designation",
        header=Template("Replace Designation"),
        line1=Template("Change the designation from to one of the following:"),
        line2=Template("")
    )


class ChangeDesignationSetup(Setup):
    pass


def change_designation_order_setup():
    return ChangeDesignationSetup(
        type="change designation at the end",
        header=Template("Change Designation order"),
        line1=Template("Change designation order to the end of the name."),
        line2=Template("")
    )


class ChangeDesignationSetup(Setup):
    pass


change_designation_order_setup = ChangeDesignationSetup(
    type="change designation at the end",
    header=Template("Change Designation order"),
    line1=Template("Change designation order to the end of the name."),
    line2=Template("")
)


class ChangeEntityTypeSetup(Setup):
    pass


def change_entity_type_setup():
    return ChangeEntityTypeSetup(
        type="change_entity_type",
        header=Template("Change Entity Type"),
        line1=Template("The designation you have selected is not appropriate for this entity type. You can choose to select a different type by pressing the 'RESTART and CHANGE TYPE' button."),
        line2=Template(""),
        label=Template("Change $entity_type to $correct_designations")
    )
