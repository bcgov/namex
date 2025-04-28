from datetime import date
from string import Template

from namex.services.name_request.auto_analyse import AnalysisIssueCodes

from ..response_objects import Conflict, NameAction, NameActions, NameAnalysisIssue

# Import DTOs
from .abstract import AnalysisResponseIssue


class CorporateNameConflictIssue(AnalysisResponseIssue):
    issue_type = AnalysisIssueCodes.CORPORATE_CONFLICT
    status_text = 'Further Action Required'
    issue = None

    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2=None,
            consenting_body=None,
            designations=None,
            show_reserve_button=None,
            show_examination_button=False,
            conflicts=[],
            setup=None,
            name_actions=[],
        )

        return issue

    def configure_issue(self, procedure_result):
        name_as_submitted = self.analysis_response.name_as_submitted
        list_original = self._lc_list_items(self.analysis_response.name_original_tokens)
        list_name = self._lc_list_items(self.analysis_response.name_tokens)

        all_designations = self._lc_list_items(self.analysis_response.analysis_service.get_all_designations())

        list_name_as_submitted = self._lc_list_items(self.analysis_response.name_as_submitted_tokenized)
        # Filter out designations from the tokens
        list_tokens = [item for item in list_name_as_submitted if item not in all_designations]

        list_dist = procedure_result.values['list_dist']  # Don't lower case this one it's a list wrapped list
        list_desc = procedure_result.values['list_desc']  # Don't lower case this one it's a list wrapped list
        list_conflicts = procedure_result.values['list_conflicts']  # Don't lower case this one it's a dict
        if procedure_result.values['source'] == 'nr':
            start_date = ''
            id_num = ''
            source = procedure_result.values['source']
        else:
            start_date = procedure_result.values['start_date']
            id_num = procedure_result.values['id']
            source = procedure_result.values['source']

        issue = self.create_issue()
        if issue.issue_type == AnalysisIssueCodes.CORPORATE_CONFLICT:
            issue.line1 = 'Too similar to an existing name.'
        else:
            issue.line1 = 'Too similar to a name currently being reviewed.'

        """
        eg:
        list_name: <class 'list'>: ['mountain', 'view', 'growers']
        list_dist: <class 'list'>: [['mountain'], ['mountain', 'view']]
        list_desc: <class 'list'>: [['view', 'growers'], ['growers']]
        list_conflicts: <class 'dict'>: {'MOUNTAIN VIEW GROWERS INC.': {'mountain': ['mountain'], 'view': ['view'], 'growers': ['growers']}}
        """

        # Grab the first conflict
        current_conflict_name = list(list_conflicts.keys())[0]  # eg: 'MOUNTAIN VIEW GROWERS INC.'
        current_conflict = list_conflicts[
            current_conflict_name
        ]  # eg: {'mountain': ['mountain'], 'view': ['view'], 'growers': ['growers']}

        current_conflict_keys = list(current_conflict.keys()) if current_conflict else []

        is_exact_match = list_name == current_conflict_keys

        list_dist_words = list(set([item for sublist in list_dist for item in sublist]))
        list_desc_words = list(set([item for sublist in list_desc for item in sublist]))

        # Apply our is_exact_match strategy:
        # - Add brackets after the first distinctive word
        # - Add brackets after the last descriptive word?
        # - Strike out the last word

        list_remove = []  # These are passed down to the Template

        if is_exact_match:
            # Loop over the token words, we need to decide to do with each word
            for token_idx, word in enumerate(list_tokens):
                offset_idx, word_idx, word_idx_offset, composite_token_offset = self.adjust_word_index(
                    name_as_submitted, list_original, list_tokens, token_idx
                )

                # Highlight the conflict words
                if list_tokens.index(word) != list_tokens.index(list_tokens[-1]):
                    issue.name_actions.append(
                        NameAction(word=word, index=offset_idx, endIndex=offset_idx, type=NameActions.HIGHLIGHT)
                    )

                # Strike out the last matching word
                if list_tokens.index(word) == list_tokens.index(list_tokens[-1]):
                    list_remove.append(word)
                    issue.name_actions.append(
                        NameAction(word=word, index=offset_idx, endIndex=offset_idx, type=NameActions.STRIKE)
                    )

        if not is_exact_match:
            # Loop over the list_name words, we need to decide to do with each word
            for token_idx, word in enumerate(list_tokens):
                offset_idx, word_idx, word_idx_offset, composite_token_offset = self.adjust_word_index(
                    name_as_submitted, list_original, list_tokens, token_idx
                )

                # This code has duplicate blocks because it allows us to tweak the response for composite token matches separately from normal words if necessary
                if composite_token_offset and composite_token_offset > 0:
                    # <class 'list'>: ['mountain', 'view']
                    # Highlight the conflict words
                    if word in current_conflict_keys and current_conflict_keys.index(
                        word
                    ) != current_conflict_keys.index(current_conflict_keys[-1]):
                        issue.name_actions.append(NameAction(word=word, index=offset_idx, type=NameActions.HIGHLIGHT))

                    # Strike out the last matching word
                    if word in current_conflict_keys and current_conflict_keys.index(
                        word
                    ) == current_conflict_keys.index(current_conflict_keys[-1]):
                        issue.name_actions.append(NameAction(word=word, index=offset_idx, type=NameActions.STRIKE))
                else:
                    # Highlight the conflict words
                    if word in current_conflict_keys and current_conflict_keys.index(
                        word
                    ) != current_conflict_keys.index(current_conflict_keys[-1]):
                        issue.name_actions.append(NameAction(word=word, index=offset_idx, type=NameActions.HIGHLIGHT))

                    # Strike out the last matching word
                    if word in current_conflict_keys and current_conflict_keys.index(
                        word
                    ) == current_conflict_keys.index(current_conflict_keys[-1]):
                        issue.name_actions.append(NameAction(word=word, index=offset_idx, type=NameActions.STRIKE))

        issue.conflicts = []

        conflict = Conflict(
            name=current_conflict_name, date=date.today(), start_date=start_date, id=id_num, source=source
        )

        issue.conflicts.append(conflict)

        # Setup boxes
        issue.setup = self.setup_config
        # Replace template strings in setup boxes
        for setup_item in issue.setup:
            # Loop over properties
            for prop in vars(setup_item):
                if isinstance(setup_item.__dict__[prop], Template):
                    # Render the Template string, replacing placeholder vars
                    setattr(
                        setup_item,
                        prop,
                        setup_item.__dict__[prop].safe_substitute(
                            {
                                'list_name': self._join_list_words(list_name),
                                'list_remove': self._join_list_words(list_remove),
                                'list_dist': self._join_list_words(list_dist_words),
                                'list_desc': self._join_list_words(list_desc_words),
                            }
                        ),
                    )

        return issue
