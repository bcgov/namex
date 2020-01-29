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

    def create_issue(self):
        issue = super(ValidNameResponseStrategy, self).create_new_issue()
        return issue


class AddDistinctiveWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.ADD_DISTINCTIVE_WORD
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(AddDistinctiveWordResponseStrategy, self).create_new_issue()
        return issue


class AddDescriptiveWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.ADD_DESCRIPTIVE_WORD
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(AddDescriptiveWordResponseStrategy, self).create_new_issue()
        return issue


class ContainsWordsToAvoidResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.WORD_TO_AVOID
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(ContainsWordsToAvoidResponseStrategy, self).create_new_issue()
        return issue


class DesignationMismatchResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.DESIGNATION_MISMATCH
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(DesignationMismatchResponseStrategy, self).create_new_issue()
        return issue


class TooManyWordsResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.TOO_MANY_WORDS
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(TooManyWordsResponseStrategy, self).create_new_issue()
        return issue


class NameRequiresConsentResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.NAME_REQUIRES_CONSENT
    status_text = 'May be Approved With Consent'

    def create_issue(self):
        issue = super(NameRequiresConsentResponseStrategy, self).create_new_issue()
        return issue


class ContainsUnclassifiableWordResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(ContainsUnclassifiableWordResponseStrategy, self).create_new_issue()
        return issue


class CorporateNameConflictResponseStrategy(AnalysisResponseStrategy):
    issue_type = AnalysisResultCodes.CORPORATE_CONFLICT
    status_text = 'Further Action Required'

    def create_issue(self):
        issue = super(CorporateNameConflictResponseStrategy, self).create_new_issue()
        return issue

