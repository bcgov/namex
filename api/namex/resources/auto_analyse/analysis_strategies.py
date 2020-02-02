from namex.services.name_request.auto_analyse import AnalysisResultCodes

# Import response base
from .analysis_response_strategy import AnalysisResponseStrategy

# Import DTOs
from .response_objects.name_analysis_issue import NameAnalysisIssue
from .response_objects.name_analysis_response import NameAnalysisResponse
from .response_objects.name_action import NameAction
from .response_objects.consenting_body import ConsentingBody
from .response_objects.conflict import Conflict
from .response_objects.descriptive_word import DescriptiveWord


class ValidNameResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.VALID_NAME
    status_text = 'Approved'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class AddDistinctiveWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class AddDescriptiveWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class ContainsWordsToAvoidResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.WORD_TO_AVOID
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class DesignationMismatchResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.DESIGNATION_MISMATCH
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class TooManyWordsResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.TOO_MANY_WORDS
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class NameRequiresConsentResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.NAME_REQUIRES_CONSENT
    status_text = 'May be Approved With Consent'
    issue = NameAnalysisIssue(
        consentingBody=ConsentingBody(
            name='Test Body',
            email='test@example.com'
        ),
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class ContainsUnclassifiableWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue


class CorporateNameConflictResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.CORPORATE_CONFLICT
    status_text = 'Further Action Required'
    issue = NameAnalysisIssue(
        consentingBody=None,
        designations=None,
        descriptiveWords=None,
        issueType=issue_type,
        word=None,
        wordIndex=None,
        showExaminationButton=None,
        conflicts=None,
        options=None,
        nameActions=None
    )

    @classmethod
    def create_issue(cls):
        issue = cls.issue
        return issue

