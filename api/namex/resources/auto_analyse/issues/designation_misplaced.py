from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

# Import DTOs
from .abstract import AnalysisResponseIssue
from ..response_objects import NameAnalysisIssue
from ..response_objects import NameAction, NameActions


class DesignationMisplacedIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_MISPLACED
    status_text = "Further Action Required"
    issue = None

    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1="",
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[]
        )

        return issue

    def configure_issue(self, procedure_result):
        # list_name_incl_designation = self.analysis_response.name_original_tokens

        misplaced_end_designation = procedure_result.values['misplaced_end_designation']
        misplaced_end_designation_lc = self._lc_list_items(misplaced_end_designation, True)
        # list_name_incl_designation_lc = self._lc_list_items(list_name_incl_designation)

        issue = self.create_issue()
        issue.line1 = "The " + self._join_list_words(misplaced_end_designation_lc) + \
                      " designation must be at the end of the name."

        # Loop over the list_name words, we need to decide to do with each word
        # for word in list_name_incl_designation_lc:
        #     offset_idx, word_idx, word_idx_offset, composite_token_offset = self.adjust_word_index(
        #         self.analysis_response.name_as_submitted,
        #         self.analysis_response.name_original_tokens,
        #         list_name_incl_designation_lc,
        #         list_name_incl_designation.index(word.lower()),
        #         False
        #     )

        #     # Highlight the issues
        #     if word in misplaced_end_designation_lc:
        #         issue.name_actions.append(NameAction(
        #             word=word,
        #             index=0,
        #             type=NameActions.HIGHLIGHT
        #         ))

        # only need incorrect phrases, don't care about where they are in the name
        for phrase in misplaced_end_designation_lc:
            issue.name_actions.append(
                NameAction(
                    word=phrase,
                    index=0,  # not used
                    type=NameActions.HIGHLIGHT  # not used
                )
            )

        # Setup boxes
        issue.setup = self.setup_config
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute([]))

        return issue
