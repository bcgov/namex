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
    CorporateNameConflictIssue, IncorrectCategory, WordSpecialUse

from namex.services.name_request.auto_analyse import AnalysisResultCodes


# Execute analysis returns a response strategy code
def response_issues(issue_code):
    issue_types = {
        AnalysisResultCodes.VALID_NAME: ValidName,
        AnalysisResultCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordIssue,
        AnalysisResultCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordIssue,
        AnalysisResultCodes.TOO_MANY_WORDS: TooManyWordsIssue,
        AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordIssue,
        AnalysisResultCodes.INCORRECT_CATEGORY: IncorrectCategory,
        AnalysisResultCodes.WORD_TO_AVOID: ContainsWordsToAvoidIssue,
        AnalysisResultCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentIssue,
        AnalysisResultCodes.DESIGNATION_MISMATCH: DesignationMismatchIssue,
        AnalysisResultCodes.CORPORATE_CONFLICT: CorporateNameConflictIssue,
        AnalysisResultCodes.WORD_SPECIAL_USE: WordSpecialUse
    }

    return issue_types.get(issue_code, ValidName)


class AnalysisResponse:
    def __init__(self, analysis_result):
        self.header = ""
        self.status_code = ""
        self.issues = []

        print(repr(analysis_result))

        if analysis_result and len(analysis_result) > 0:
            for procedure_result in analysis_result:
                if callable(response_issues(procedure_result.result_code)):
                    issue_builder = response_issues(procedure_result.result_code)
                    response_issue = issue_builder.create_issue(procedure_result)
                    if response_issue and response_issue.issue_type is not AnalysisResultCodes.VALID_NAME:
                        self.issues.append(response_issue)
                    else:
                        pass

        # TODO: This is an incomplete implementation! Get returned status codes from ProcedureResult
        status_code = "fa"

        if status_code == "fa":
            self.status_code = "fa"
            self.header = "Further Action Required"

    def prepare_payload(self):
        payload = NameAnalysisResponse(
            header=self.header,
            status=self.status_code,
            issues=self.issues
        )
        return payload

    '''
    This is invoked by consumers of this class
    '''
    def build_response(self):
        response = self.prepare_payload()
        return response
