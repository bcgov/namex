from namex.services.name_request.auto_analyse import AnalysisResultCodes

# Import DTOs
from .response_objects.name_analysis_issue import NameAnalysisIssue
from .response_objects.name_analysis_response import NameAnalysisResponse
from .response_objects.name_action import NameAction, NameActions, WordPositions
from .response_objects.consenting_body import ConsentingBody
from .response_objects.conflict import Conflict
from .response_objects.descriptive_word import DescriptiveWord


class AnalysisResponseIssue:
    issue_type = 'Issue'  # Maybe get rid of this guy
    header = 'Further Action Required'
    status_text = ''
    status = ''  # This is a CODE [AV | FA | RC]
    issue = None

    def __init__(self):
        pass

    @classmethod
    def create_issue(cls):
        return cls.issue


class ValidName(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.VALID_NAME
    status_text = 'Approved'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=None,
        conflicts=None,
        setup=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class AddDistinctiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=None,
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.START,
                message='Add a Word Here"'
            )
        ]

        return issue


class AddDescriptiveWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=[],
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=None,
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.END,
                message='Add a Business Category Word Here'
            )
        ]

        return issue


class ContainsWordsToAvoidIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.WORD_TO_AVOID
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=None,
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.STRIKE
            )
        ]

        return issue


class DesignationMismatchIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.DESIGNATION_MISMATCH
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=[],
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=None,
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.STRIKE
            )
        ]

        return issue


class TooManyWordsIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.TOO_MANY_WORDS
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=True,
        conflicts=None,
        setup=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class NameRequiresConsentIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.NAME_REQUIRES_CONSENT
    status_text = 'May be Approved With Consent'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=ConsentingBody(
            name='Example Inc.',
            email='test@example.com'
        ),
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=None,
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.HIGHLIGHT
            )
        ]

        return issue


class ContainsUnclassifiableWordIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=True,
        conflicts=None,
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.STRIKE
            )
        ]

        return issue


class CorporateNameConflictIssue(AnalysisResponseIssue):
    issue_type = AnalysisResultCodes.CORPORATE_CONFLICT
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        line1=None,
        line2=None,
        consentingBody=None,
        designations=None,
        # descriptive# words=None,
        issueType=issue_type,
        # words=None,
        # wordIndex=None,
        showReserveButton=None,
        showExaminationButton=False,
        conflicts=[],
        setup=None,
        nameActions=[]
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue

        issue.nameActions = [
            NameAction(
                type=NameActions.STRIKE
            ),
            NameAction(
                type=NameActions.BRACKETS,
                position=WordPositions.START,
                message='Add a Word Here'
            )
        ]

        # Create conflicts
        conflict = Conflict(
            name='Test Conflict',
            date=''
        )

        issue.conflicts = []
        issue.conflicts.append(conflict)

        return issue

