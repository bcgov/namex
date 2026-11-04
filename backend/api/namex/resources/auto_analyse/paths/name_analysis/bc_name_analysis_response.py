from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ... import QueueNameConflictIssue
from ...analysis_options import (
    add_descriptive_setup,
    add_designation_setup,
    add_distinctive_setup,
    change_designation_order_setup,
    change_entity_type_setup,
    conflict_self_consent_setup,
    obtain_consent_setup,
    remove_designation_setup,
    remove_or_replace_setup,
    remove_setup,
    replace_designation_setup,
    resolve_conflict_setup,
    send_to_examiner_setup,
    too_many_words_setup,
)
from ...analysis_response import AnalysisResponse

# Execute analysis returns a response strategy code
from ...issues.designation_removal import DesignationRemovalIssue
from .issues import (
    BcAddDescriptiveWordIssue as AddDescriptiveWordIssue,
)
from .issues import (
    BcAddDistinctiveWordIssue as AddDistinctiveWordIssue,
)
from .issues import (
    BcCheckIsValidIssue as CheckIsValidIssue,
)
from .issues import (
    BcContainsUnclassifiableWordIssue as ContainsUnclassifiableWordIssue,
)
from .issues import (
    BcContainsWordsToAvoidIssue as ContainsWordsToAvoidIssue,
)
from .issues import (
    BcCorporateNameConflictIssue as CorporateNameConflictIssue,
)
from .issues import (
    BcDesignationMismatchIssue as DesignationMismatchIssue,
)
from .issues import (
    BcDesignationMisplacedIssue as DesignationMisplacedIssue,
)
from .issues import (
    BcDesignationNonExistentIssue as DesignationNonExistentIssue,
)
from .issues import (
    BcEndDesignationMoreThanOnceIssue as EndDesignationMoreThanOnceIssue,
)
from .issues import (
    BcIncorrectCategoryIssue as IncorrectCategoryIssue,
)
from .issues import (
    BcIncorrectYearIssue as IncorrectYearIssue,
)
from .issues import (
    BcNameRequiresConsentIssue as NameRequiresConsentIssue,
)
from .issues import (
    BcTooManyWordsIssue as TooManyWordsIssue,
)
from .issues import (
    BcWordSpecialUseIssue as WordSpecialUseIssue,
)


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
        AnalysisIssueCodes.WORD_SPECIAL_USE: WordSpecialUseIssue,
    }

    return issue_types.get(issue_code, CheckIsValidIssue)


class BcAnalysisResponse(AnalysisResponse):
    def build_unclassified_word_issue(self, procedure_result, issue_count, issue_idx):
        is_only_issue = self.is_only_issue(issue_count, issue_idx)
        has_next_issue = self.has_next_issue(issue_count, issue_idx)

        issue = None

        # If there's only one issue, display helpful hint and the examination button
        if is_only_issue:
            option1 = remove_or_replace_setup()

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])

            issue.show_examination_button = True
        elif has_next_issue:
            option1 = remove_or_replace_setup()

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])
        elif not is_only_issue and has_next_issue is False:
            option1 = remove_or_replace_setup()

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_add_distinctive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_distinctive_setup()

        option2 = send_to_examiner_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1, option2])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_add_descriptive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_descriptive_setup()

        option2 = send_to_examiner_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1, option2])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_too_many_words_issue(self, procedure_result, issue_count, issue_idx):
        option1 = too_many_words_setup()
        # Tweak the header
        option1.header = 'Required Action'

        issue = response_issues(procedure_result.result_code)(self, [])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_incorrect_year_issue(self, procedure_result, issue_count, issue_idx):
        option1 = send_to_examiner_setup()

        issue = response_issues(procedure_result.result_code)(
            self,
            [
                option1,
            ],
        )

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_words_to_avoid_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_setup()
        option1.header = 'Required Action'

        issue = response_issues(procedure_result.result_code)(self, [option1])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_name_requires_consent_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_or_replace_setup()

        option2 = send_to_examiner_setup()

        option3 = obtain_consent_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1, option2, option3])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_corporate_conflict_issue(self, procedure_result, issue_count, issue_idx):
        option1 = resolve_conflict_setup()

        option2 = send_to_examiner_setup()

        option3 = conflict_self_consent_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1, option2, option3])

        """
        # Quick tests for overriding button behavior
        if issue_count > 1:
            issue.show_reserve_button = True
            issue.show_examination_button = False
        else:
            issue.show_reserve_button = True
            issue.show_examination_button = False
        """

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_queue_conflict_issue(self, procedure_result, issue_count, issue_idx):
        option1 = resolve_conflict_setup()

        option2 = conflict_self_consent_setup()

        issue = response_issues(procedure_result.result_code)(
            self,
            [
                option1,
                option2,
            ],
        )

        """
        # Quick tests for overriding button behavior
        if issue_count > 1:
            issue.show_reserve_button = True
            issue.show_examination_button = False
        else:
            issue.show_reserve_button = True
            issue.show_examination_button = False
        """

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_non_existent_designation_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_designation_setup()
        option1.header = 'Required Action'

        issue = response_issues(procedure_result.result_code)(self, [option1])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_designation_mismatch_issue(self, procedure_result, issue_count, issue_idx):
        option1 = replace_designation_setup()

        option2 = change_entity_type_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1, option2])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_designation_removal_issue(self, procedure_result, issue_count, issue_idx):
        option1 = remove_designation_setup(procedure_result.values.get('incorrect_designations', []))

        option2 = change_entity_type_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1, option2])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_end_designation_more_than_once_issue(self, procedure_result, issue_count, issue_idx):
        option1 = send_to_examiner_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1])
        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_designation_misplaced_issue(self, procedure_result, issue_count, issue_idx):
        option1 = change_designation_order_setup()
        option1.header = 'Required Action'

        issue = response_issues(procedure_result.result_code)(self, [option1])

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

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])

            issue.show_examination_button = True
        elif has_next_issue:
            option1 = remove_or_replace_setup()

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])
        elif not is_only_issue and has_next_issue is False:
            option1 = remove_or_replace_setup()

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue
