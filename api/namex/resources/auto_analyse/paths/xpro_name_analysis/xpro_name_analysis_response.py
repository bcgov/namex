from ...analysis_response import AnalysisResponse

from .issues import \
    XproCheckIsValidIssue as CheckIsValidIssue, \
    XproAddDistinctiveWordIssue as AddDistinctiveWordIssue, \
    XproAddDescriptiveWordIssue as AddDescriptiveWordIssue, \
    XproContainsWordsToAvoidIssue as ContainsWordsToAvoidIssue, \
    XproDesignationMismatchIssue as DesignationMismatchIssue, \
    XproTooManyWordsIssue as TooManyWordsIssue, \
    XproNameRequiresConsentIssue as NameRequiresConsentIssue, \
    XproContainsUnclassifiableWordIssue as ContainsUnclassifiableWordIssue, \
    XproCorporateNameConflictIssue as CorporateNameConflictIssue, \
    XproIncorrectCategoryIssue as IncorrectCategoryIssue, \
    XproWordSpecialUseIssue as WordSpecialUseIssue, \
    XproDesignationMisplacedIssue as DesignationMisplacedIssue, \
    XproDesignationNonExistentIssue as DesignationNonExistentIssue

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ...analysis_options import \
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
        AnalysisIssueCodes.CHECK_IS_VALID: CheckIsValidIssue,
        AnalysisIssueCodes.ADD_DISTINCTIVE_WORD: AddDistinctiveWordIssue,
        AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD: AddDescriptiveWordIssue,
        AnalysisIssueCodes.TOO_MANY_WORDS: TooManyWordsIssue,
        AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD: ContainsUnclassifiableWordIssue,
        AnalysisIssueCodes.INCORRECT_CATEGORY: IncorrectCategoryIssue,
        AnalysisIssueCodes.WORDS_TO_AVOID: ContainsWordsToAvoidIssue,
        AnalysisIssueCodes.NAME_REQUIRES_CONSENT: NameRequiresConsentIssue,
        AnalysisIssueCodes.DESIGNATION_NON_EXISTENT: DesignationNonExistentIssue,
        AnalysisIssueCodes.DESIGNATION_MISMATCH: DesignationMismatchIssue,
        AnalysisIssueCodes.DESIGNATION_MISPLACED: DesignationMisplacedIssue,
        AnalysisIssueCodes.CORPORATE_CONFLICT: CorporateNameConflictIssue,
        AnalysisIssueCodes.WORD_SPECIAL_USE: WordSpecialUseIssue
    }

    return issue_types.get(issue_code, CheckIsValidIssue)


class XproAnalysisResponse(AnalysisResponse):
    def build_unclassified_word_issue(self, procedure_result, issue_count, issue_idx):
        is_only_issue = self.is_only_issue(issue_count, issue_idx)
        has_next_issue = self.has_next_issue(issue_count, issue_idx)

        issue = None

        # If there's only one issue, display helpful hint and the examination button
        if is_only_issue:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self, [
                option1,
                option2
            ])
        elif has_next_issue:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self, [
                option1,
                option2
            ])
        elif not is_only_issue and has_next_issue is False:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self, [
                option1,
                option2
            ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_add_distinctive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_distinctive_setup()
        # Tweak the header
        option1.header = "Helpful Tip"

        issue = response_issues(procedure_result.result_code)(self, [
            option1
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_add_descriptive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_descriptive_setup()
        # Tweak the header
        option1.header = "Helpful Tip"

        issue = response_issues(procedure_result.result_code)(self, [
            option1
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_too_many_words_issue(self, procedure_result, issue_count, issue_idx):
        option1 = too_many_words_setup()
        # Tweak the header
        option1.header = "Helpful Tip"

        issue = response_issues(procedure_result.result_code)(self, [
            option1
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_words_to_avoid_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_setup()
        # Tweak the header
        option1.header = "Helpful Tip"

        issue = response_issues(procedure_result.result_code)(self, [
            option1
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_name_requires_consent_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_or_replace_setup()
        # Tweak the header
        option1.header = "Option 1"

        option2 = send_to_examiner_setup()
        # Tweak the header
        option2.header = "Option 2"

        option3 = obtain_consent_setup()
        # Tweak the header
        option3.header = "Option 3"

        issue = response_issues(procedure_result.result_code)(self, [
            option1,
            option2,
            option3
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_corporate_conflict_issue(self, procedure_result, issue_count, issue_idx):
        option1 = resolve_conflict_setup()
        # Tweak the header
        option1.header = "Option 1"

        option2 = send_to_examiner_setup()
        # Tweak the header
        option2.header = "Option 2"

        option3 = conflict_self_consent_setup()
        # Tweak the header
        option3.header = "Option 3"

        issue = response_issues(procedure_result.result_code)(self, [
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

    def build_non_existent_designation_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_designation_setup()
        # Tweak the header
        option1.header = "Option 1"

        issue = response_issues(procedure_result.result_code)(self, [
            option1
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_designation_mismatch_issue(self, procedure_result, issue_count, issue_idx):
        option1 = replace_designation_setup()
        # Tweak the header
        option1.header = "Option 1"

        option2 = change_entity_type_setup()
        # Tweak the header
        option2.header = "Option 2"

        issue = response_issues(procedure_result.result_code)(self, [
            option1,
            option2
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_designation_misplaced_issue(self, procedure_result, issue_count, issue_idx):
        option1 = change_designation_order_setup()
        # Tweak the header
        option1.header = "Option 1"

        issue = response_issues(procedure_result.result_code)(self, [
            option1
        ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_word_special_use_issue(self, procedure_result, issue_count, issue_idx):
        is_only_issue = self.is_only_issue(issue_count, issue_idx)
        has_next_issue = self.has_next_issue(issue_count, issue_idx)

        issue = None

        # If there's only one issue, display helpful hint and the examination button
        if is_only_issue:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self, [
                option1,
                option2
            ])
        elif has_next_issue:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self, [
                option1,
                option2
            ])
        elif not is_only_issue and has_next_issue is False:
            option1 = remove_or_replace_setup()
            # Tweak the header
            option1.header = "Option 1"

            option2 = send_to_examiner_setup()
            # Tweak the header
            option2.header = "Option 2"

            issue = response_issues(procedure_result.result_code)(self, [
                option1,
                option2
            ])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue
