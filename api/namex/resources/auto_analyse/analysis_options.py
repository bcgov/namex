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
    header="",
    line1="Add Distinctive",
    line2=""
)


class AddDescriptiveSetup(Setup):
    pass


add_descriptive_setup = AddDistinctiveSetup(
    type="add_descriptive",
    header="",
    line1="Add Descriptive",
    line2=""
)


class TooManyWordsSetup(Setup):
    pass


too_many_words_setup = TooManyWordsSetup(
    type="too_many_words",
    header="",
    line1="Too Many Words",
    line2=""
)


class RemoveOrReplaceSetup(Setup):
    pass


remove_or_replace_setup = RemoveOrReplaceSetup(
    type="remove_or_replace",
    header="",
    line1="Remove or Replace",
    line2=""
)


class SendToExaminerSetup(Setup):
    pass


send_to_examiner_setup = SendToExaminerSetup(
    type="send_to_examiner",
    header="",
    line1="Send to Examiner",
    line2="",
    label=""
)


class ObtainConsentSetup(Setup):
    pass


obtain_consent_setup = ObtainConsentSetup(
    type="obtain_consent",
    header="",
    line1="Obtain Consent",
    line2="",
    label="I am able to obtain and send written consent."
)


class SelfConsentSetup(Setup):
    pass


self_consent_setup = SelfConsentSetup(
    type="self_consent",
    header="",
    line1="Self Consent",
    line2="",
    label="I have authority over the conflicting name."
)


class ReplaceDesignationSetup(Setup):
    pass


replace_designation_setup = ReplaceDesignationSetup(
    type="replace_designation",
    header="",
    line1="Replace Designation",
    line2="",
    label=""
)


class ChangeEntityTypeSetup(Setup):
    pass


change_entity_type_setup = ChangeEntityTypeSetup(
    type="change_entity_type",
    header="",
    line1="Change Entity Type",
    line2="",
    label=""
)