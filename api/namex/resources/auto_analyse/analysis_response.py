# Import DTOs
from .response_objects.name_analysis_response import NameAnalysisResponse
from ..auto_analyse.analysis_issues import \
    ValidName, \
    AddDistinctiveWordIssue, \
    AddDescriptiveWordIssue, \
    ContainsWordsToAvoidIssue, \
    DesignationMismatchIssue, \
    TooManyWordsIssue, \
    NameRequiresConsentIssue, \
    ContainsUnclassifiableWordIssue, \
    CorporateNameConflictIssue

from namex.services.name_request.auto_analyse import AnalysisResultCodes


# Execute analysis returns a response strategy code
def response_issues(strategy):
    strategies = {
        AnalysisResultCodes.VALID_NAME: ValidName,
        AnalysisResultCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordIssue,
        AnalysisResultCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordIssue,
        AnalysisResultCodes.TOO_MANY_WORDS: TooManyWordsIssue,
        AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordIssue,
        AnalysisResultCodes.WORD_TO_AVOID: ContainsWordsToAvoidIssue,
        AnalysisResultCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentIssue,
        AnalysisResultCodes.DESIGNATION_MISMATCH: DesignationMismatchIssue,
        AnalysisResultCodes.CORPORATE_CONFLICT: CorporateNameConflictIssue
    }
    return strategies.get(strategy, ValidName)


class AnalysisResponse:
    def __init__(self, analysis_result):
        self.status_text = ''
        self.issues = []

        print(repr(analysis_result))

        for issue in analysis_result:
            issue_builder = response_issues(issue.result_code)
            if callable(issue_builder):
                response_issue = issue_builder(issue)
                if response_issue:
                    self.issues.append(response_issue.create_issue())

    def prepare_payload(self):
        payload = NameAnalysisResponse(
            status=self.status_text,
            issues=self.issues
        )
        return payload

    '''
    This is invoked by consumers of this class
    '''
    def build_response(self):
        response = self.prepare_payload()
        return response
