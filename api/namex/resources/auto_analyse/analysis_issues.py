from datetime import date

from namex.services.name_request.auto_analyse import AnalysisResultCodes

# Import DTOs
from .response_objects.name_analysis_issue import NameAnalysisIssue
from .response_objects.name_analysis_response import NameAnalysisResponse
from .response_objects.name_action import NameAction, NameActions, WordPositions
from .response_objects.consenting_body import ConsentingBody
from .response_objects.conflict import Conflict
from .response_objects.setup import Setup
from .response_objects.descriptive_word import DescriptiveWord


class AnalysisResponseIssue:
    issue_type = "Issue"  # Maybe get rid of this guy
    header = "Further Action Required"
    status_text = ""
    status = ""  # This is a CODE [AV | FA | RC]
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
        issueType=issue_type,
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue
        return issue


class AddDistinctiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="Requires a word at the beginning of your name that sets it apart.",
        line2=None,
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=False,
        showExaminationButton=False,
        conflicts=None,
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.ADD_WORD_BRACKETS,
                position=WordPositions.START,
                message="Add a Word Here"
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Helpful Hint",
                line1="Some words that can set your name apart include an individual's name or intials; a geographic location; a colour; a coined, made-up word; or an acronym.",
                line2=""
            )
        ]

        return issue


class AddDescriptiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="Requires a Business Category Word",
        line2=None,
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=False,
        showExaminationButton=False,
        conflicts=None,
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.ADD_WORD_BRACKETS,
                position=WordPositions.END,
                message="Add a Descriptive Word Here"
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Helpful Hint",
                line1="Some words that can set your name apart include an individual's name or intials; a geographic location; a colour; a coined, made-up word; or an acronym.",
                line2=""
            )
        ]

        return issue


class ContainsWordsToAvoidIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.WORD_TO_AVOID
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="Your name contains words that cannot be approved:",
        line2="Walmart",
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=False,
        showExaminationButton=False,
        conflicts=None,
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.STRIKE
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Helpful Hint",
                line1="Remove the word <b>Walmart</b> from your search and try again.",
                line2=""
            )
        ]

        return issue


class DesignationMismatchIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.DESIGNATION_MISMATCH
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="Designation <b>Cooperative</b> cannot be used with selected business type of <b>Corporation</b>",
        line2=None,
        consentingBody=None,
        # TODO: Replace with real values from ProcedureResult
        designations=[
            "Inc",
            "Incorporated",
            "Incorpore",
            "Limite",
            "Limited",
            "Ltd"
        ],
        # words=None,
        # wordIndex=None,
        showReserveButton=False,
        showExaminationButton=False,
        conflicts=None,
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Option 1",
                line1="If your intention was to reserve a name for a BC Corporation, you can replace Cooperative with a comptatible designation. The following are allowed:",
                line2=""
            ),
            Setup(
                button="restart",
                checkbox="",
                heading="Option 2",
                line1="If you would like to start a Cooperative business instead of a Corporation, start your search over and change your business type to 'Cooperative'.",
                line2=""
            )
        ]

        return issue


class TooManyWordsIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.TOO_MANY_WORDS
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="This name is too long to be auto-approved.",
        line2=None,
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=False,
        showExaminationButton=True,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Helpful Hint",
                line1="You can remove one or more words and try your search again, or you can choose to submit the name above for examination.",
                line2=""
            )
        ]

        return issue


class NameRequiresConsentIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.NAME_REQUIRES_CONSENT
    status_text = "May be Approved With Consent"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1=None,
        line2=None,
        consentingBody=ConsentingBody(
            name="Example Inc.",
            email="test@example.com"
        ),
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=None,
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        issue.consentingBody = ConsentingBody(
            name="Association of Professional Engineers of BC",
            email="email@engineer.ca"
        )

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Option 1",
                line1="You can remove or replace the word “Engineering” and try your search again.",
                line2=""
            ),
            Setup(
                button="examine",
                checkbox="",
                heading="Option 2",
                line1="You can choose to submit this name for examination. Examination wait times are listed above.",
                line2=""
            ),
            Setup(
                button="consent",
                checkbox="",
                heading="Option 3",
                line1="This name can be auto-approved but you will be required to send confirmation of consent to the BC Business Registry.",
                line2=""
            )
        ]

        return issue


class ContainsUnclassifiableWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="<b>Flerkin</b> is an unknown word.  The system cannot auto-approve a name with unknown words.",
        line2="It might still be approvable by manual examination.",
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=False,
        showExaminationButton=True,
        conflicts=None,
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        # Setup boxes
        issue.setup = [
            Setup(
                button="",
                checkbox="",
                heading="Helpful Hint",
                line1="You can remove or replace the word <b>Flerkin</b> and try your search again.  Alternately, you can submit your name for examination-wait times are quoted above.",
                line2=""
            )
        ]

        return issue


class CorporateNameConflictIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.CORPORATE_CONFLICT
    status_text = "Further Action Required"
    issue = NameAnalysisIssue(
        issueType=issue_type,
        line1="Too similar to an existing name.",
        line2=None,
        consentingBody=None,
        designations=None,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=[],
        options=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls, procedure_result):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.STRIKE
            ),
            NameAction(
                type=NameActions.ADD_WORD_BRACKETS,
                position=WordPositions.START,
                message="Add a Word Here"
            )
        ]

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
                heading="Option 1",
                line1="Add a word to the beginning of the name that sets it apart like a person's name or initials.",
                line2="Or remove ${some-word} and replace it with a different word"
            ),
            Setup(
                button="examine",
                checkbox="",
                heading="Option 2",
                line1="You can choose to submit this name for examination. Examination wait times are listed above.",
                line2=""
            ),
            Setup(
                button="consent",
                checkbox="",
                heading="Option 3",
                line1="If you are the registered owner of the existing name, it can be auto-approved but you are required to send confirmation of consent to the BC Business Registry.",
                line2=""
            )
        ]

        return issue
