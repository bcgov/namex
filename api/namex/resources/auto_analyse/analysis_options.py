from .response_objects.setup import Setup


class HelpfulHintSetup(Setup):
    pass


helpful_hint_setup = HelpfulHintSetup(
    type="helpful_hint",
    header="",
    line1="Helpful Hint",
    line2=""
)


class AddDistinctiveSetup(Setup):
    pass


add_distinctive_setup = AddDistinctiveSetup(
    type="add_distinctive",
    header="Add Distinctive",
    line1="Add some words to the beginning of your name that sets your name apart. For example, an individual's name or initials; a geographic location; a colour; a coined, made-up word; or an acronym.",
    line2="Example: Change 'Renovations Ltd.' → 'Joe's Renovations Ltd."
)


class AddDescriptiveSetup(Setup):
    pass


add_descriptive_setup = AddDistinctiveSetup(
    type="add_descriptive",
    header="Add Descriptive",
    line1="Add some additional words that help describe what your business does. For example, the product or service you provide.",
    line2="Example: Change 'Joe's Ltd.' → 'Joe's Renovations Ltd."
)


class TooManyWordsSetup(Setup):
    pass


too_many_words_setup = TooManyWordsSetup(
    type="too_many_words",
    header="Too Many Words",
    line1="Please remove one or more words and try your search again, or you can choose to submit the name above for examination.",
    line2="Note: Designations at the end of your name such as 'Limited', 'Inc', 'Cooperative' will not be counted."
)


class RemoveSetup(Setup):
    pass


remove_setup = RemoveSetup(
    type="remove",
    header="Remove",
    line1="Please remove or replace the word from your search and try again.",
    line2=""
)


class RemoveOrReplaceSetup(Setup):
    pass


remove_or_replace_setup = RemoveOrReplaceSetup(
    type="remove_or_replace",
    header="Remove or Replace",
    line1="Please remove or replace the highlighted words and try your search again.",
    line2=""
)


class RemoveOrSubmitSetup(Setup):
    pass


remove_or_submit_setup = RemoveOrReplaceSetup(
    type="remove_or_submit",
    header="Remove or Submit",
    line1="Please remove or replace the highlighted words and try your search again, or you can choose to submit the name above for examination.",
    line2=""
)


class ResolveConflictSetup(Setup):
    pass


resolve_conflict_setup = ResolveConflictSetup(
    type="resolve_conflict",
    header="Resolve Conflict",
    line1="Add a word to the beginning of the name that sets it apart like a person’s name or initials.",
    line2="Or remove the word(s) {words} and replace them with different ones."
)


class SendToExaminerSetup(Setup):
    pass


send_to_examiner_setup = SendToExaminerSetup(
    type="send_to_examiner",
    header="Send to Examiner",
    line1="You can choose to submit this name for examination. Please check wait times at the top of the screen.",
    line2="",
    action="I want my name examined."
)


class ObtainConsentSetup(Setup):
    pass


obtain_consent_setup = ObtainConsentSetup(
    type="obtain_consent",
    header="Obtain Consent",
    line1="This name can be auto-approved, but you will be required to send written consent to the BC Business Registry.",
    line2="",
    action="I am able to obtain and send written consent."
)


class SelfConsentSetup(Setup):
    pass


conflict_self_consent_setup = SelfConsentSetup(
    type="conflict_self_consent",
    header="Conflict Self Consent",
    line1="This name can be auto-approved if you are the registered owner of the conflicting name, but you are required to send written consent to the BC Business Registry.",
    line2="",
    action="I am the registered owner of the conflicting name. I will send written consent."
)


class ReplaceDesignationSetup(Setup):
    pass


replace_designation_setup = ReplaceDesignationSetup(
    type="replace_designation",
    header="Replace Designation",
    line1="Replace Designation",
    line2=""
)


class ChangeEntityTypeSetup(Setup):
    pass


change_entity_type_setup = ChangeEntityTypeSetup(
    type="change_entity_type",
    header="Change Entity Type",
    line1="Change Entity Type",
    line2=""
)