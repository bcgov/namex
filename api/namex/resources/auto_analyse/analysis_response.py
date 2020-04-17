# Import DTOs
from .response_objects.name_analysis_response import NameAnalysisResponse
from ..auto_analyse.analysis_issues import \
    CheckIsValid, \
    AddDistinctiveWordIssue, \
    AddDescriptiveWordIssue, \
    ContainsWordsToAvoidIssue, \
    DesignationMismatchIssue, \
    TooManyWordsIssue, \
    NameRequiresConsentIssue, \
    ContainsUnclassifiableWordIssue, \
    CorporateNameConflictIssue, \
    IncorrectCategory, \
    WordSpecialUse, \
    DesignationMisplacedIssue, \
    DesignationNonExistentIssue

from namex.services.name_request.auto_analyse import AnalysisIssueCodes, AnalysisResponseCodes

from .analysis_options import \
    helpful_hint_setup, \
    add_distinctive_setup, \
    add_descriptive_setup, \
    too_many_words_setup, \
    remove_setup, \
    remove_or_replace_setup, \
    resolve_conflict_setup, \
    send_to_examiner_setup, \
    obtain_consent_setup, \
    conflict_self_consent_setup, \
    replace_designation_setup, \
    change_entity_type_setup, \
    change_designation_order_setup, \
    add_designation_setup


# Execute analysis returns a response strategy code
def response_issues(issue_code):
    issue_types = {
        AnalysisIssueCodes.CHECK_IS_VALID: CheckIsValid,
        AnalysisIssueCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordIssue,
        AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordIssue,
        AnalysisIssueCodes.TOO_MANY_WORDS: TooManyWordsIssue,
        AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordIssue,
        AnalysisIssueCodes.INCORRECT_CATEGORY: IncorrectCategory,
        AnalysisIssueCodes.WORDS_TO_AVOID: ContainsWordsToAvoidIssue,
        AnalysisIssueCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentIssue,
        AnalysisIssueCodes.DESIGNATION_NON_EXISTENT: DesignationNonExistentIssue,
        AnalysisIssueCodes.DESIGNATION_MISMATCH: DesignationMismatchIssue,
        AnalysisIssueCodes.DESIGNATION_MISPLACED: DesignationMisplacedIssue,
        AnalysisIssueCodes.CORPORATE_CONFLICT: CorporateNameConflictIssue,
        AnalysisIssueCodes.WORD_SPECIAL_USE: WordSpecialUse
    }

    return issue_types.get(issue_code, CheckIsValid)


class AnalysisResponse:
    @classmethod
    def _has_next_issue(cls, issue_count, issue_idx):
        return issue_idx + 1 < issue_count

    @classmethod
    def _is_only_issue(cls, issue_count, issue_idx):
        return (issue_idx + 1) == issue_count == 1

    def _build_unclassified_word_issue(self, procedure_result, issue_count, issue_idx):
        is_only_issue = self._is_only_issue(issue_count, issue_idx)
        has_next_issue = self._has_next_issue(issue_count, issue_idx)

        issue = None

        # If there's only one issue, display helpful hint and the examination button
        if is_only_issue:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self.entity_type, [
                option1,
                option2,
                # option3
            ])

            issue.show_examination_button = True
        elif has_next_issue:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self.entity_type, [
                option1,
                option2,
                # option3
            ])
        elif not is_only_issue and has_next_issue is False:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self.entity_type, [
                option1,
                option2,
                # option3
            ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_add_distinctive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_distinctive_setup()
        # Tweak the header
        option1.header = "Helpful Tip"
        # option2 = None
        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            # option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_add_descriptive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_descriptive_setup()
        # Tweak the header
        option1.header = "Helpful Tip"
        # option2 = None
        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            # option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_too_many_words_issue(self, procedure_result, issue_count, issue_idx):
        option1 = too_many_words_setup()
        # Tweak the header
        option1.header = "Helpful Tip"
        # option2 = None
        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            # option2 = None
            # option3 = None
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_words_to_avoid_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_setup()
        # Tweak the header
        option1.header = "Helpful Tip"
        # option2 = None
        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            # option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_name_requires_consent_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_or_replace_setup()
        # Tweak the header
        option1.header = "Option 1"

        option2 = send_to_examiner_setup()
        # Tweak the header
        option2.header = "Option 2"

        option3 = obtain_consent_setup()
        # Tweak the header
        option3.header = "Option 3"

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            option2,
            option3
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_corporate_conflict_issue(self, procedure_result, issue_count, issue_idx):
        option1 = resolve_conflict_setup()
        # Tweak the header
        option1.header = "Option 1"

        option2 = send_to_examiner_setup()
        # Tweak the header
        option2.header = "Option 2"

        option3 = conflict_self_consent_setup()
        # Tweak the header
        option3.header = "Option 3"

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            option2,
            option3
        ])

        '''
        # Quick tests for overriding button behavior
        if issue_count > 1:
            issue.show_reserve_button = True
            issue.show_examination_button = False
        else:
            issue.show_reserve_button = True
            issue.show_examination_button = False
        '''

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_non_existent_designation_issue(self, procedure_result, issue_count, issue_idx):
        # option1 = add_designation_setup()
        option1 = replace_designation_setup()
        # Tweak the header
        option1.header = "Option 1"

        # option2 = None
        # Tweak the header

        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            #option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_designation_mismatch_issue(self, procedure_result, issue_count, issue_idx):
        option1 = replace_designation_setup()
        # Tweak the header
        option1.header = "Option 1"

        option2 = change_entity_type_setup()
        # Tweak the header
        option2.header = "Option 2"

        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_designation_misplaced_issue(self, procedure_result, issue_count, issue_idx):
        option1 = change_designation_order_setup()
        # Tweak the header
        option1.header = "Option 1"

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            option1,
            # option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def _build_word_special_use_issue(self, procedure_result, issue_count, issue_idx):
        # option1 = None
        # option2 = None
        # option3 = None

        issue = response_issues(procedure_result.result_code)(self.entity_type, [
            # option1,
            # option2,
            # option3
        ])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    '''
    @:param analysis_result ProcedureResult[]
    '''

    def __init__(self, entity_type, analysis_result):
        self.entity_type = entity_type
        self.header = ""
        self.status_code = ""
        self.issues = []
        self.executed_procedures = []

        print(repr(analysis_result))

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
                        issue = self._build_unclassified_word_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.ADD_DISTINCTIVE_WORD:
                        issue = self._build_add_distinctive_word_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD:
                        issue = self._build_add_descriptive_word_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.TOO_MANY_WORDS:
                        issue = self._build_too_many_words_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.WORDS_TO_AVOID:
                        issue = self._build_words_to_avoid_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.NAME_REQUIRES_CONSENT:
                        issue = self._build_name_requires_consent_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.CORPORATE_CONFLICT:
                        issue = self._build_corporate_conflict_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_MISMATCH:
                        issue = self._build_designation_mismatch_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_MISPLACED:
                        issue = self._build_designation_misplaced_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.DESIGNATION_NON_EXISTENT:
                        issue = self._build_non_existent_designation_issue(procedure_result, issue_count, issue_idx)

                    if procedure_result.result_code == AnalysisIssueCodes.WORD_SPECIAL_USE:
                        issue = self._build_word_special_use_issue(procedure_result, issue_count, issue_idx)

                    response_issue = None

                    if issue:
                        response_issue = issue.create_issue(procedure_result)
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
