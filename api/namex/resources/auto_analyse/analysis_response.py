import abc

# Import DTOs
from .response_objects.name_analysis_response import NameAnalysisResponse
from ..auto_analyse.analysis_issues import \
    CheckIsValidIssue, \
    AddDistinctiveWordIssue, \
    AddDescriptiveWordIssue, \
    ContainsWordsToAvoidIssue, \
    DesignationMismatchIssue, \
    DesignationRemovalIssue,\
    TooManyWordsIssue, \
    NameRequiresConsentIssue, \
    ContainsUnclassifiableWordIssue, \
    CorporateNameConflictIssue, \
    IncorrectCategoryIssue, \
    WordSpecialUseIssue, \
    DesignationMisplacedIssue, \
    EndDesignationMoreThanOnceIssue, \
    DesignationNonExistentIssue, \
    QueueNameConflictIssue, \
    IncorrectYearIssue

from namex.services.name_request.auto_analyse import AnalysisIssueCodes, AnalysisResponseCodes


# Execute analysis returns a response strategy code
def response_issues(issue_code):
    issue_types = {
        AnalysisIssueCodes.CHECK_IS_VALID: CheckIsValidIssue,
        AnalysisIssueCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordIssue,
        AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordIssue,
        AnalysisIssueCodes.TOO_MANY_WORDS: TooManyWordsIssue,
        AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordIssue,
        AnalysisIssueCodes.INCORRECT_CATEGORY: IncorrectCategoryIssue,
        AnalysisIssueCodes.INCORRECT_YEAR: IncorrectYearIssue,
        AnalysisIssueCodes.WORDS_TO_AVOID: ContainsWordsToAvoidIssue,
        AnalysisIssueCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentIssue,
        AnalysisIssueCodes.DESIGNATION_NON_EXISTENT: DesignationNonExistentIssue,
        AnalysisIssueCodes.DESIGNATION_MISMATCH: DesignationMismatchIssue,
        AnalysisIssueCodes.DESIGNATION_REMOVAL: DesignationRemovalIssue,
        AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE: EndDesignationMoreThanOnceIssue,
        AnalysisIssueCodes.DESIGNATION_MISPLACED: DesignationMisplacedIssue,
        AnalysisIssueCodes.CORPORATE_CONFLICT: CorporateNameConflictIssue,
        AnalysisIssueCodes.QUEUE_CONFLICT: QueueNameConflictIssue,
        AnalysisIssueCodes.WORD_SPECIAL_USE: WordSpecialUseIssue
    }

    return issue_types.get(issue_code, CheckIsValidIssue)


class AnalysisResponse:
    @property
    def analysis_service(self):
        return self._analysis_service

    @analysis_service.setter
    def analysis_service(self, analysis_service):
        self._analysis_service = analysis_service

    @property
    def name_tokens(self):
        return self.analysis_service.name_tokens

    @property
    def name_original_tokens(self):
        return self.analysis_service.name_original_tokens

    @property
    def processed_name(self):
        return self.analysis_service.processed_name

    @property
    def name_as_submitted(self):
        return self.analysis_service.name_as_submitted

    @property
    def name_as_submitted_tokenized(self):
        return self.analysis_service.name_as_submitted_tokenized

    @property
    def entity_type(self):
        return self._entity_type

    @entity_type.setter
    def entity_type(self, entity_type):
        self._entity_type = entity_type

    @classmethod
    def has_next_issue(cls, issue_count, issue_idx):
        return issue_idx + 1 < issue_count

    @classmethod
    def is_only_issue(cls, issue_count, issue_idx):
        return (issue_idx + 1) == issue_count == 1

    @abc.abstractmethod
    def build_unclassified_word_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_add_distinctive_word_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_add_descriptive_word_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_incorrect_year_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_too_many_words_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_words_to_avoid_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_name_requires_consent_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_corporate_conflict_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_queue_conflict_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_non_existent_designation_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_designation_mismatch_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_designation_removal_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_end_designation_more_than_once_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_designation_misplaced_issue(self, procedure_result, issue_count, issue_idx):
        return None

    @abc.abstractmethod
    def build_word_special_use_issue(self, procedure_result, issue_count, issue_idx):
        return None


    '''
    @:param analysis_result ProcedureResult[]
    '''

    def __init__(self, analysis_service, analysis_result):
        self.analysis_service = analysis_service
        self.entity_type = analysis_service.entity_type
        self.header = ""
        self.status_code = ""
        self.issues = []
        self.executed_procedures = []

        is_valid_name_request = True
        issue_count = len(analysis_result)
        issue_idx = None

        if analysis_result and issue_count > 0:
            for result_idx, procedure_result in enumerate(analysis_result):
                if callable(response_issues(procedure_result.result_code)):
                    # Pass in params?
                    issue = None
                    issue_idx = result_idx

                    if procedure_result.result_code == AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD:
                        issue = self.build_unclassified_word_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.ADD_DISTINCTIVE_WORD:
                        issue = self.build_add_distinctive_word_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD:
                        issue = self.build_add_descriptive_word_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.INCORRECT_YEAR:
                        issue = self.build_incorrect_year_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.TOO_MANY_WORDS:
                        issue = self.build_too_many_words_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.WORDS_TO_AVOID:
                        issue = self.build_words_to_avoid_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.NAME_REQUIRES_CONSENT:
                        issue = self.build_name_requires_consent_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.CORPORATE_CONFLICT:
                        issue = self.build_corporate_conflict_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.QUEUE_CONFLICT:
                        issue = self.build_queue_conflict_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_MISMATCH:
                        issue = self.build_designation_mismatch_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_REMOVAL:
                        issue = self.build_designation_removal_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.END_DESIGNATION_MORE_THAN_ONCE:
                        issue = self.build_end_designation_more_than_once_issue(procedure_result,issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_MISPLACED:
                        issue = self.build_designation_misplaced_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_NON_EXISTENT:
                        issue = self.build_non_existent_designation_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.WORD_SPECIAL_USE:
                        issue = self.build_word_special_use_issue(procedure_result, issue_count, issue_idx)

                    response_issue = None

                    if issue:
                        response_issue = issue.configure_issue(procedure_result)
                        # TODO: This seems redundant doing this on the backend
                        if not result_idx == len(analysis_result) - 1:
                            response_issue.show_next_button = True

                    if response_issue and response_issue.issue_type is not AnalysisIssueCodes.CHECK_IS_VALID:
                        # We know what the issues are? Now how do we apply the setup types
                        self.issues.append(response_issue)
                        is_valid_name_request = False

        # TODO: This is an incomplete implementation! Get returned status codes from ProcedureResult
        if not is_valid_name_request:
            self.status_code = AnalysisResponseCodes.FURTHER_ACTION_REQUIRED.value
            self.header = "Further Action Required"
        else:
            self.status_code = AnalysisResponseCodes.AUTO_APPROVED.value
            self.header = "Available"

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
