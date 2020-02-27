from datetime import date

from namex.services.name_request.auto_analyse import AnalysisResultCodes

# Import DTOs
from .response_objects.name_analysis_issue import NameAnalysisIssue
from .response_objects.name_action import NameAction, NameActions, WordPositions
from .response_objects.consenting_body import ConsentingBody
from .response_objects.conflict import Conflict
from .response_objects.setup import Setup


class AnalysisResponseIssue:
    issue_type = "Issue"  # Maybe get rid of this guy
    header = "Further Action Required"
    status_text = ""
    status = "fa"  # This is a CODE [AV | FA | RC]
    issue = None

    def __init__(self):
        pass

    @classmethod
    def create_issue(cls, procedure_result):
        return cls.issue


class ValidName(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.VALID_NAME
    status_text = "Approved"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1=None,
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=None,
        show_examination_button=None,
        conflicts=None,
        setup=None,
        name_actions=None
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue
        return issue


"""
Word Classification Engine Issues
"""


class IncorrectCategory(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.INCORRECT_CATEGORY
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Category of the word is incorrect.",
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=True,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.name_actions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="You can change the the order of the word <b>Flerkin</b> and try your search again.  Alternately, you can submit your name for examination-wait times are quoted above.",
                line2=""
            )
        ]

        return issue


"""
Well-Formed Name Issues
"""


class ContainsUnclassifiableWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="The submitted name contains unknown words. The system cannot auto-approve a name with unknown words.",
        line2="It might still be approvable by manual examination.",
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=True,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue
        list_name = procedure_result.values['list_name']
        list_none = procedure_result.values['list_none']

        cls.issue.line1 = "The word(s) <b>" + ", ".join(list_none) + "</b> are unknown. The system cannot auto-approve a name with unknown words."

        # TODO: Fix the case eg. 'Asdfadsf Something Asdfadsf Company Ltd.'...
        #  If there's a duplicate of an unclassified word, just grabbing the index won't do!
        issue.name_actions = []
        for word in list_none:
            none_word_idx = list_name.index(word)
            issue.name_actions.append(
                NameAction(
                    type=NameActions.HIGHLIGHT,
                    word=word,
                    index=none_word_idx
                )
            )

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="You can remove or replace the words <b>" + ", ".join(list_none) + "</b> and try your search again.  Alternately, you can submit your name for examination-wait times are quoted above.",
                line2=""
            )
        ]

        return issue


class AddDistinctiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Requires a word at the beginning of your name that sets it apart.",
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=False,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue
        values = procedure_result.values

        issue.name_actions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.START,
                message="Add a Word Here",
                word=values[0],
                index=0
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="Some words that can set your name apart include an individual's name or intials; a geographic location; a colour; a coined, made-up word; or an acronym.",
                line2=""
            )
        ]

        return issue


class AddDescriptiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Requires a Business Category Word",
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=False,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue
        list_name = procedure_result.values['list_name']
        list_dist = procedure_result.values['list_dist']

        last_dist_word = list_dist.pop()
        dist_word_idx = list_name.index(last_dist_word)
        issue.name_actions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.END,
                message="Add a Descriptive Word Here",
                word=last_dist_word,
                index=dist_word_idx
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="Some words that can set your name apart include an individual's name or intials; a geographic location; a colour; a coined, made-up word; or an acronym.",
                line2=""
            )
        ]

        return issue


class TooManyWordsIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.TOO_MANY_WORDS
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="This name is too long to be auto-approved.",
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=True,
        conflicts=None,
        setup=None,
        name_actions=None
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="You can remove one or more words and try your search again, or you can choose to submit the name above for examination.",
                line2=""
            )
        ]

        return issue


"""
General Name Issues
"""


class ContainsWordsToAvoidIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.WORD_TO_AVOID
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Your name contains words that cannot be approved:",
        line2="Walmart",
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=False,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.name_actions = [
            NameAction(
                type=NameActions.STRIKE
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="Remove the word <b>Walmart</b> from your search and try again.",
                line2=""
            )
        ]

        return issue


class WordSpecialUse(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.WORD_SPECIAL_USE
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Words do not require consent but can only be used under certain content.",
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=False,
        show_examination_button=True,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.name_actions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Helpful Hint",
                line1="You can use the word <b>Doctor</b> under certain conditions, you might remove it.  Alternately, you can submit your name for examination-wait times are quoted above.",
                line2=""
            )
        ]

        return issue


class NameRequiresConsentIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.NAME_REQUIRES_CONSENT
    status_text = "May be Approved With Consent"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1=None,
        line2=None,
        consenting_body=ConsentingBody(
            name="",
            email=""
        ),
        designations=None,
        show_reserve_button=None,
        show_examination_button=False,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue
        list_name = procedure_result.values['list_name']
        list_consent = procedure_result.values['list_consent']

        # TODO: Everything else lets the backend dictate the response message, using line1 and line2 except this one...
        issue.line1 = "The word(s) <b>" + ", ".join(list_consent) + "</b> require consent from:"
        issue.line2 = "Example Conflict Company Ltd.<br />" + "email@example.com"

        issue.name_actions = []
        for word in list_consent:
            consent_word_idx = list_name.index(word)
            issue.name_actions.append(
                NameAction(
                    type=NameActions.HIGHLIGHT,
                    word=word,
                    index=consent_word_idx
                )
            )

        # TODO: Where does this info come from?
        issue.consenting_body = ConsentingBody(
            name="Example Conflict Company Ltd.",
            email="email@example.com"
        )

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Option 1",
                line1="You can remove or replace the word(s) " + ", ".join(list_consent) + " and try your search again.",
                line2=""
            ),
            Setup(
                button="examine",
                checkbox="",
                header="Option 2",
                line1="You can choose to submit this name for examination. Examination wait times are listed above.",
                line2=""
            ),
            Setup(
                button="consent",
                checkbox="",
                header="Option 3",
                line1="This name can be auto-approved but you will be required to send confirmation of consent to the BC Business Registry.",
                line2=""
            )
        ]

        return issue


class CorporateNameConflictIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.CORPORATE_CONFLICT
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Too similar to an existing name.",
        line2=None,
        consenting_body=None,
        designations=None,
        show_reserve_button=None,
        show_examination_button=False,
        conflicts=[],
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        # TODO: What is the conflicting word(s)
        #  - index, position

        issue.name_actions = []

        index = 0
        word = 'Mountain'
        position = WordPositions.START

        issue.name_actions.append(NameAction(
            word=word,
            index=index,
            type=NameActions.STRIKE
        ))

        index = 1
        word = 'Mountain'
        position = WordPositions.START

        issue.name_actions.append(NameAction(
            word=word,
            index=index,
            type=NameActions.BRACKETS,
            position=position,
            message="Add a Word Here"
        ))

        # Create conflicts
        # TODO: Check if it is a list
        if procedure_result.values:
            issue.conflicts = []

            for value in procedure_result.values:
                conflict = Conflict(
                    name=value,
                    date=date.today()
                )

                issue.conflicts.append(conflict)

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Option 1",
                line1="Add a word to the beginning of the name that sets it apart like a person's name or initials.",
                line2="Or remove ${some-word} and replace it with a different word"
            ),
            Setup(
                button="examine",
                checkbox="",
                header="Option 2",
                line1="You can choose to submit this name for examination. Examination wait times are listed above.",
                line2=""
            ),
            Setup(
                button="consent",
                checkbox="",
                header="Option 3",
                line1="If you are the registered owner of the existing name, it can be auto-approved but you are required to send confirmation of consent to the BC Business Registry.",
                line2=""
            )
        ]

        return issue


class DesignationMismatchIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.DESIGNATION_MISMATCH
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issue_type=issue_type,
        line1="Designation <b>Cooperative</b> cannot be used with selected business type of <b>Corporation</b>",
        line2=None,
        consenting_body=None,
        # TODO: Replace with real values from ProcedureResult
        designations=[
            "Inc",
            "Incorporated",
            "Incorpore",
            "Limite",
            "Limited",
            "Ltd"
        ],
        show_reserve_button=False,
        show_examination_button=False,
        conflicts=None,
        setup=None,
        name_actions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.name_actions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                header="Option 1",
                line1="If your intention was to reserve a name for a BC Corporation, you can replace Cooperative with a comptatible designation. The following are allowed:",
                line2=""
            ),
            Setup(
                button="restart",
                checkbox="",
                header="Option 2",
                line1="If you would like to start a Cooperative business instead of a Corporation, start your search over and change your business type to 'Cooperative'.",
                line2=""
            )
        ]

        return issue

