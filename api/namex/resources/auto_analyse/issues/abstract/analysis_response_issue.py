import abc
import re
from collections import deque

from flask import current_app

# Import DTOs
from ...response_objects import NameAnalysisIssue


class AnalysisResponseIssue:
    issue_type = 'Issue'  # Maybe get rid of this guy
    header = 'Further Action Required'
    status_text = ''
    status = 'fa'  # This is a CODE [AV | FA | RC]
    issue = None

    """
    @:param setup_config Setup[]
    """

    def __init__(self, analysis_response, setup_config):
        self.analysis_response = analysis_response
        self.name_tokens = analysis_response.name_tokens
        self.entity_type = analysis_response.entity_type
        self.setup_config = []
        self.set_issue_setups(setup_config)

    # TODO: Maybe move this to utils? Do as part of code clean up and refactor task
    @classmethod
    def _lc_list_items(cls, str_list, convert=False):
        if not str_list or type(str_list) is not list:
            return []  # This method should always return a list

        try:
            converted_list = (
                [d.upper() if isinstance(d, str) else '' for d in str_list]
                if convert
                else [d.upper() for d in str_list]
            )
        except Exception as err:
            current_app.logger.error('List is not a list of strings ' + repr(err))

        return converted_list

    @abc.abstractmethod
    def create_issue(self):
        issue = NameAnalysisIssue(
            issue_type=self.issue_type,
            line1='',
            line2='',
            consenting_body=None,
            designations=None,
            show_next_button=False,
            show_reserve_button=False,
            show_examination_button=False,
            conflicts=None,
            setup=None,
            name_actions=[],
        )

        return issue

    @abc.abstractmethod
    def configure_issue(self, procedure_result):
        return self.issue

    """
    @:param setup_config Setup[]
    """

    def set_issue_setups(self, setup_config):
        self.setup_config = setup_config

    @classmethod
    def _join_list_words(cls, list_words, separator=', '):
        return '<b>' + separator.join(list_words) + '</b>'

    # Johnson & Johnson Engineering will return original tokens:
    # [Johnson, &, Johnson, Engineering]
    # and return name tokens:
    # [Johnson, Engineering]

    # Johnson & Johnson & Johnson Engineering will return original tokens:
    # [Johnson, &, Johnson, &, Johnson, Engineering]
    # and return name tokens:
    # [Johnson, Engineering]

    # John Deere Deere Engineering will return original tokens:
    # [John, Deere, Deere, Engineering]
    # and return name tokens:
    # [John, Deere, Engineering]

    # John Deere & Deere Engineering will return original tokens:
    # [John, Deere, &, Deere, Engineering]
    # and return name tokens:
    # [John, Deere, Engineering]

    # John Deere John Engineering will return original tokens:
    # [John, Deere, John, Engineering]
    # and return name tokens:
    # [John, Deere, John, Engineering]

    # J & L Engineering will return original tokens:
    # [J, &, L, Engineering]
    # and return name tokens:
    # [JL, Engineering]

    # J & L & L Engineering will return original tokens:
    # [J, &, L, &, L, Engineering]
    # and return name tokens:
    # [JLL, Engineering]
    def get_next_token_if_composite(self, str_name, name_original_tokens, name_processed_tokens):
        token_string = ''
        processed_name_string = ''

        original_tokens = deque(name_original_tokens)
        processed_tokens = deque(name_processed_tokens)

        if len(processed_tokens) == 0:
            return False, 0, 0, None

        processed_token = processed_tokens.popleft()
        current_processed_token = processed_token

        processed_token_count = 0
        composite_idx_offset = 0
        current_original_token = original_tokens.popleft()

        if current_processed_token == current_original_token:
            return False, 0, 0, current_original_token

        if current_processed_token.find(current_original_token) == -1:
            return False, 0, 0, current_original_token

        while len(original_tokens) > 0:
            if token_string == processed_token:
                break

            processed_token_count += 1

            processed_name_string += current_original_token

            token_substr_idx = current_processed_token.find(current_original_token)
            token_is_next_chunk = token_substr_idx == 0
            if token_is_next_chunk:
                current_processed_token = current_processed_token[len(current_original_token) :]
                token_string += current_original_token

            next_char = False
            # To get the current character use something like: this_char = str_name[len(original_name_string) - 1]
            if len(str_name) > len(processed_name_string):
                next_char = str_name[len(processed_name_string)]

            if next_char and next_char == ' ':
                processed_name_string += ' '

            if next_char and next_char == ' ' or not next_char:
                composite_idx_offset += 1

            if len(original_tokens) > 0:
                current_original_token = original_tokens.popleft()

        if processed_token_count:
            return processed_token, processed_token_count, composite_idx_offset, processed_name_string

        return False, 0, 0, current_processed_token

    def adjust_word_index(
        self, original_name_str, name_original_tokens, name_tokens, word_idx, offset_designations=True
    ):
        # remove punctuations
        name_original_tokens = [re.sub(r'(?<=[a-zA-Z\.])\'[Ss]', '', x) for x in name_original_tokens]
        name_original_tokens = [re.sub(r'[^A-Za-z0-9.]+', ' ', x) for x in name_original_tokens]

        all_designations = self.analysis_response.analysis_service.get_all_designations()

        all_designations = self._lc_list_items(all_designations)
        list_original = self._lc_list_items(name_original_tokens)

        name_tokens = self._lc_list_items(name_tokens)
        # all_designations_user = self.analysis_response.analysis_service.get_all_designations_user()

        original_tokens = deque(list_original)
        processed_tokens = deque(name_tokens)
        processed_token_idx = 0

        target_word = name_tokens[word_idx]

        word_idx_offset = 0
        composite_token_offset = 0

        previous_original_token = None
        current_original_token = None

        unprocessed_name_string = original_name_str.upper()

        while len(original_tokens) > 0:
            # Check to see if we're dealing with a composite, if so, get the offset amount
            composite_token, composite_tokens_processed, composite_idx_offset, processed_name_string = (
                self.get_next_token_if_composite(unprocessed_name_string, original_tokens, processed_tokens)
            )

            if processed_name_string:
                # Only replace the first match!
                unprocessed_name_string = re.sub(
                    r'{0}(\'[Ss])?'.format(processed_name_string), '', unprocessed_name_string, count=1
                ).strip()

            # Handle composite tokens
            if composite_token:
                current_original_token = composite_token

                if composite_idx_offset > 0:
                    composite_token_offset += composite_idx_offset - 1

                for _x in range(0, composite_tokens_processed):
                    if len(original_tokens) > 0:
                        original_tokens.popleft()

            # Handle normal word tokens
            else:
                if len(original_tokens) > 0:
                    # Pop the left-most token off the list
                    current_original_token = original_tokens.popleft()

                    # If there are no processed tokens left to deal with, skip this step (handles designations, etc.)
                    # We don't need to increment the word_idx_offset anymore unless there's a repeated token
                    if len(processed_tokens) > 0:
                        if offset_designations:
                            # Does the current word have any punctuation associated with?
                            next_char = ''
                            if (
                                len(unprocessed_name_string) > 0
                                and len(original_tokens) > 0
                                and unprocessed_name_string[0] == original_tokens[0]
                            ):
                                next_char = original_tokens[0]

                            token_is_designation = (current_original_token + next_char) in all_designations
                            if original_tokens and token_is_designation:
                                # original_tokens.popleft()
                                unprocessed_name_string = unprocessed_name_string.strip()

                            # Skip designations
                            if token_is_designation or current_original_token not in name_tokens:
                                word_idx_offset += 1
                                continue
                        else:
                            if current_original_token not in name_tokens:
                                word_idx_offset += 1
                                continue

            # Check for repeated tokens - this has been moved to get_next_token_if_composite
            if current_original_token == previous_original_token:
                word_idx_offset += 1

            # We only need to run this until we encounter the specified word
            if current_original_token == target_word and word_idx == processed_token_idx:
                original_tokens.clear()  # Clear the rest of the items to break out of the loop, we're done!
                continue

            # if previous_original_token != current_original_token and len(processed_tokens) > 0:
            if len(processed_tokens) > 0 and current_original_token != previous_original_token:
                processed_token_idx += 1
                processed_tokens.popleft()

            previous_original_token = current_original_token

        offset_idx = word_idx + word_idx_offset + composite_token_offset

        current_app.logger.debug(
            'Adjusted word index for word ['
            + target_word
            + '] from ['
            + str(word_idx)
            + '] -> ['
            + str(offset_idx)
            + ']'
        )

        return offset_idx, word_idx, word_idx_offset, composite_token_offset
