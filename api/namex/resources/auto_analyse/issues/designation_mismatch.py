from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from namex.utils.entity_type import get_entity_type_description

# Import DTOs
from .abstract import AnalysisResponseIssue
from ..response_objects import NameAnalysisIssue
from ..response_objects import NameAction, NameActions


class DesignationMismatchIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.DESIGNATION_MISMATCH
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
        list_name = self.analysis_response.name_tokens
        # list_name_incl_designation = self.analysis_response.name_original_tokens

        incorrect_designations = procedure_result.values['incorrect_designations']
        correct_designations = procedure_result.values['correct_designations']

        incorrect_designations_lc = self._lc_list_items(incorrect_designations, True)
        correct_designations_lc = self._lc_list_items(correct_designations, True)
        # list_name_incl_designation_lc = self._lc_list_items(list_name_incl_designation)

        entity_type_description = get_entity_type_description(self.entity_type)

        issue = self.create_issue()
        issue.line1 = "The " + self._join_list_words(incorrect_designations_lc) + " designation cannot be used for a " + entity_type_description + " </b>."
        issue.designations = correct_designations_lc

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

        #     if word in incorrect_designations_lc:
        #         issue.name_actions.append(NameAction(
        #             word=word,
        #             index=0,
        #             type=NameActions.HIGHLIGHT
        #         ))
        # only need incorrect phrases, don't care about where they are in the name
        for phrase in incorrect_designations_lc:
            issue.name_actions.append(
                NameAction(
                    word=phrase,
                    index=0,  # not used
                    type=NameActions.HIGHLIGHT  # not used
                )
            )

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(setup_item, prop, setup_item.__dict__[prop].safe_substitute({
                        'list_name': self._join_list_words(list_name),
                        'correct_designations': self._join_list_words(correct_designations_lc),
                        'incorrect_designations': self._join_list_words(incorrect_designations_lc),
                        'entity_type_cd': self.entity_type  # TODO: Map this CODE!
                    }))

        return issue
