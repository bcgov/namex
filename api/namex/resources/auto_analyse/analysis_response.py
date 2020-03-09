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
    change_entity_type_setup


# Execute analysis returns a response strategy code
def response_issues(issue_code):
    issue_types = {
        AnalysisResultCodes.VALID_NAME: ValidName,
        AnalysisResultCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordIssue,
        AnalysisResultCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordIssue,
        AnalysisResultCodes.TOO_MANY_WORDS: TooManyWordsIssue,
        AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordIssue,
        AnalysisResultCodes.INCORRECT_CATEGORY: IncorrectCategory,
        AnalysisResultCodes.WORDS_TO_AVOID: ContainsWordsToAvoidIssue,
        AnalysisResultCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentIssue,
        AnalysisResultCodes.DESIGNATION_MISMATCH: DesignationMismatchIssue,
        AnalysisResultCodes.CORPORATE_CONFLICT: CorporateNameConflictIssue,
        AnalysisResultCodes.WORD_SPECIAL_USE: WordSpecialUse
    }

    return issue_types.get(issue_code, ValidName)


class AnalysisResponse:
    '''
    @:param analysis_result ProcedureResult[]
    '''
    def __init__(self, analysis_result):
        self.header = ""
        self.status_code = ""
        self.issues = []

        print(repr(analysis_result))

        executed_procedures = []

        is_valid_name_request = False
        if analysis_result and len(analysis_result) > 0:
            for result_idx, procedure_result in enumerate(analysis_result):
                if callable(response_issues(procedure_result.result_code)):
                    # Pass in params?
                    issue_builder = None

                    option1 = None  # When assigning, use a preconfigured setup type
                    option2 = None  # When assigning, use a preconfigured setup type
                    option3 = None  # When assigning, use a preconfigured setup type

                    if procedure_result.result_code == AnalysisResultCodes.CONTAINS_UNCLASSIFIABLE_WORD:
                        option1 = remove_or_replace_setup
                        # Tweak the header
                        option1.header = "Helpful Tip"
                        # option2 = None
                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            # option2,
                            # option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.ADD_DISTINCTIVE_WORD:
                        option1 = add_distinctive_setup
                        # Tweak the header
                        option1.header = "Helpful Tip"
                        # option2 = None
                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            # option2,
                            # option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.ADD_DESCRIPTIVE_WORD:
                        option1 = add_descriptive_setup
                        # Tweak the header
                        option1.header = "Helpful Tip"
                        # option2 = None
                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            # option2,
                            # option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.TOO_MANY_WORDS:
                        option1 = too_many_words_setup
                        # Tweak the header
                        option1.header = "Helpful Tip"
                        # option2 = None
                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            # option2 = None
                            # option3 = None
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.WORDS_TO_AVOID:
                        option1 = remove_setup
                        # Tweak the header
                        option1.header = "Helpful Tip"
                        # option2 = None
                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            # option2,
                            # option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.NAME_REQUIRES_CONSENT:
                        option1 = remove_or_replace_setup
                        # Tweak the header
                        option1.header = "Option 1"

                        option2 = send_to_examiner_setup
                        # Tweak the header
                        option2.header = "Option 2"

                        option3 = obtain_consent_setup
                        # Tweak the header
                        option3.header = "Option 3"

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            option2,
                            option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.CORPORATE_CONFLICT:
                        option1 = resolve_conflict_setup
                        # Tweak the header
                        option1.header = "Option 1"

                        option2 = send_to_examiner_setup
                        # Tweak the header
                        option2.header = "Option 2"

                        option3 = conflict_self_consent_setup
                        # Tweak the header
                        option3.header = "Option 3"

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            option2,
                            option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.result_code == AnalysisResultCodes.DESIGNATION_MISMATCH:
                        option1 = replace_designation_setup
                        # Tweak the header
                        option1.header = "Option 1"

                        option2 = change_entity_type_setup
                        # Tweak the header
                        option2.header = "Option 2"

                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            option1,
                            option2,
                            # option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    # TODO: Is this a real thing?
                    if procedure_result.result_code == AnalysisResultCodes.WORD_SPECIAL_USE:
                        # option1 = None
                        # option2 = None
                        # option3 = None

                        issue_builder = response_issues(procedure_result.result_code)([
                            # option1,
                            # option2,
                            # option3
                        ])
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    if procedure_result.is_valid == AnalysisResultCodes.VALID_NAME:
                        issue_builder = response_issues(procedure_result.result_code)()
                        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
                        executed_procedures.append(procedure_result.result_code)

                    response_issue = None

                    if issue_builder:
                        response_issue = issue_builder.create_issue(procedure_result)
                        # TODO: This seems redundant doing this on the backend
                        if not result_idx == len(analysis_result) - 1:
                            response_issue.show_next_button = True

                    if response_issue and response_issue.issue_type is not AnalysisResultCodes.VALID_NAME:
                        # We know what the issues are? Now how do we apply the setup types
                        self.issues.append(response_issue)
                    else:
                        is_valid_name_request = True
                        break

        # TODO: This is an incomplete implementation! Get returned status codes from ProcedureResult
        if not is_valid_name_request:
            self.status_code = "fa"
            self.header = "Further Action Required"
        else:
            self.status_code = "Available"
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
