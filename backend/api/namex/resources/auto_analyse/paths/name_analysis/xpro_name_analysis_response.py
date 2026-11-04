from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ... import QueueNameConflictIssue
from ...analysis_options import (
    add_descriptive_setup,
    add_designation_setup,
    add_distinctive_setup,
    change_designation_order_setup,
    change_entity_type_setup,
    obtain_consent_setup,
    remove_or_replace_setup,
    remove_setup,
    replace_designation_setup,
    send_to_examiner_setup,
    too_many_words_setup,
)
from ...analysis_response import AnalysisResponse
from .issues import (
    XproAddDescriptiveWordIssue as AddDescriptiveWordIssue,
)
from .issues import (
    XproAddDistinctiveWordIssue as AddDistinctiveWordIssue,
)
from .issues import (
    XproCheckIsValidIssue as CheckIsValidIssue,
)
from .issues import (
    XproContainsUnclassifiableWordIssue as ContainsUnclassifiableWordIssue,
)
from .issues import (
    XproContainsWordsToAvoidIssue as ContainsWordsToAvoidIssue,
)
from .issues import (
    XproCorporateNameConflictIssue as CorporateNameConflictIssue,
)
from .issues import (
    XproDesignationMismatchIssue as DesignationMismatchIssue,
)
from .issues import (
    XproDesignationMisplacedIssue as DesignationMisplacedIssue,
)
from .issues import (
    XproDesignationNonExistentIssue as DesignationNonExistentIssue,
)
from .issues import (
    XproIncorrectCategoryIssue as IncorrectCategoryIssue,
)
from .issues import (
    XproNameRequiresConsentIssue as NameRequiresConsentIssue,
)
from .issues import (
    XproTooManyWordsIssue as TooManyWordsIssue,
)
from .issues import (
    XproWordSpecialUseIssue as WordSpecialUseIssue,
)


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
        AnalysisIssueCodes.QUEUE_CONFLICT: QueueNameConflictIssue,
        AnalysisIssueCodes.WORD_SPECIAL_USE: WordSpecialUseIssue,
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

            option2 = send_to_examiner_setup()

            issue = response_issues(procedure_result.result_code)(self, [option1, option2])
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

        issue = response_issues(procedure_result.result_code)(self, [option1])

        # Add the procedure to the stack of executed_procedures so we know what issues have been set up
        self.executed_procedures.append(procedure_result.result_code)

        return issue

    def build_add_descriptive_word_issue(self, procedure_result, issue_count, issue_idx):
        option1 = add_descriptive_setup()

        issue = response_issues(procedure_result.result_code)(self, [option1])

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
        """
        For the XPRO path, corp_conflict issue type Options must change. Option 2 and 3 should be removed.
        Change the Helpful Hint to:
        Extra provincial or registration of a foreign entity in BC requires use of an Assumed Name when there is an existing BC entity with a similar name.

        Option 1: (Same text)
        New setup button: Need a checkbox for assumed_name. The front-end should should turn the checkbox into" I want to send my name to be examined as an Assumed Name.
        :param procedure_result:
        :param issue_count:
        :param issue_idx:
        :return:
        """
        # option1 = assumed_name_setup() if self.entity_type in (
        #     EntityTypes.XPRO_CORPORATION.value, EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value,
        #     EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value) \
        #     else alternative_assumed_name_setup()

        option1 = send_to_examiner_setup()

        option2 = obtain_consent_setup()

        issue = response_issues(procedure_result.result_code)(
            self,
            [
                option1,
                option2,
                # option3
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

    def build_queue_conflict_issue(self, procedure_result, issue_count, issue_idx):
        # option1 = assumed_name_setup() if self.entity_type in (
        #     EntityTypes.XPRO_CORPORATION.value, EntityTypes.XPRO_UNLIMITED_LIABILITY_COMPANY.value,
        #     EntityTypes.XPRO_LIMITED_LIABILITY_COMPANY.value) \
        #     else alternative_assumed_name_setup()

        option1 = send_to_examiner_setup()

        option2 = obtain_consent_setup()

        issue = response_issues(procedure_result.result_code)(
            self,
            [
                option1,
                option2,
                # option3
            ],
        )

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

    def build_designation_misplaced_issue(self, procedure_result, issue_count, issue_idx):
        option1 = change_designation_order_setup()
        # Tweak the header
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
