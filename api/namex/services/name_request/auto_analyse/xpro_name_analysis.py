import os
from datetime import datetime

from flask import current_app

from . import AnalysisIssueCodes, request_types
from .mixins.set_designation_lists import SetDesignationsListsMixin
from .name_analysis_director import NameAnalysisDirector
from .name_analysis_utils import get_classification


'''
The XproNameAnalysisService returns an analysis response using the strategies in analysis_strategies.py
The response API return cases are as follows:

- Name Contains a Word To Avoid
- Designation Mismatch
- Too Many Words
- Name Requires Consent
- Contains Unclassifiable Word
- Conflicts with the Corporate Database

Notes:
- The 'algorithm' / process we use to analyse names may change in the future
- Using the builder pattern allows us delegate and isolate custom / changing business logic to the builder,
  while exposing a consistent API for consumers of the service.
'''

d = datetime.now()  # Was just used for perf analysis

class XproNameAnalysisService(NameAnalysisDirector, SetDesignationsListsMixin):
    _d = d  # Just used for perf

    def __init__(self):
        super(XproNameAnalysisService, self).__init__()

    '''
    This is the main execution call that wraps name analysis checks.
    - Perform checks to ensure the name is well formed.
    - If the name is well formed, proceed with our analysis by calling do_analysis.
    - If you don't want to check to see if a name is well formed first, override check_name_is_well_formed in the supplied builder.
    @:return ProcedureResult[]
    '''

    def execute_analysis(self):
        try:
            builder = self.builder
            syn_svc = self.synonym_service
            wc_svc = self.word_classification_service
            token_svc = self.token_classifier_service
            np_svc = self._name_processing_service
            stand_alone_words = np_svc.get_stand_alone_words()

            analysis = []

            # Configure the analysis for the supplied builder
            get_classification(self, stand_alone_words, syn_svc, self.name_tokens, wc_svc, token_svc)

            auto_analyze_config = current_app.config.get('AUTO_ANALYZE_CONFIG')

            if auto_analyze_config in ('WELL_FORMED_NAME', 'EXACT_MATCH', 'SEARCH_CONFLICTS'):
                check_words_to_avoid = builder.check_words_to_avoid(self.name_tokens, self.processed_name)
                if not check_words_to_avoid.is_valid:
                    analysis.append(check_words_to_avoid)
                    return analysis

                # We conduct the same check for well formed names but report just search conflicts for extra-provincial names
                check_conflict_in_name_is_well_formed = builder.check_name_is_well_formed(
                    self._dict_name_words,
                    self._list_dist_words,
                    self._list_desc_words,
                    self.name_tokens,
                    self.processed_name,
                    self.name_original_tokens
                )
                if check_conflict_in_name_is_well_formed.result_code == AnalysisIssueCodes.CORPORATE_CONFLICT:
                    analysis.append(check_conflict_in_name_is_well_formed)
                    return analysis

                check_word_limit = builder.check_word_limit(self.name_tokens)
                if not check_word_limit.is_valid:
                    analysis.append(check_word_limit)
                    return analysis

                # If the error coming back is that a name is not well formed
                # OR if the error coming back has words to avoid...
                # eg. result.result_code = AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD
                # don't return the result yet, the name is well formed, we just have an unclassified
                # word in the result.

                issues_that_must_be_fixed = [
                    AnalysisIssueCodes.WORDS_TO_AVOID,
                    AnalysisIssueCodes.TOO_MANY_WORDS
                ]

                issue_must_be_fixed = False
                result_codes = list(map(lambda r: r.result_code, analysis))

                for code in result_codes:
                    if code in issues_that_must_be_fixed:
                        issue_must_be_fixed = True
                        break

                if issue_must_be_fixed:
                    return analysis
                    #  Name is not well formed - do not continue

                # If the WORD_TO_AVOID check failed, the UNCLASSIFIED_WORD check
                # will have failed too because words to avoid are never classified.
                # Strip out the unclassified words errors involving the same name words.
                list_avoid = []

                has_words_to_avoid = self._has_analysis_issue_type(analysis, AnalysisIssueCodes.WORDS_TO_AVOID)
                if has_words_to_avoid:
                    matched_words_to_avoid = \
                        self._get_analysis_issue_type_issues(analysis, AnalysisIssueCodes.WORDS_TO_AVOID)

                    for procedure_result in matched_words_to_avoid:
                        list_avoid = list_avoid + procedure_result.values.get('list_avoid', [])

                    def remove_words_to_avoid(result):
                        if result.result_code == AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD:
                            for word in list_avoid:
                                result.values['list_none'].remove(word)
                        return result

                    analysis = list(map(remove_words_to_avoid, analysis))

                analysis_issues_sort_order = [
                    AnalysisIssueCodes.WORDS_TO_AVOID,
                    AnalysisIssueCodes.TOO_MANY_WORDS,
                    AnalysisIssueCodes.WORD_SPECIAL_USE,
                    AnalysisIssueCodes.NAME_REQUIRES_CONSENT,
                    AnalysisIssueCodes.QUEUE_CONFLICT,
                    AnalysisIssueCodes.CORPORATE_CONFLICT,
                    # We don't need to check for designations, so we're skipping those codes here..
                ]

            analysis = analysis + self.do_analysis()
            analysis = self.sort_analysis_issues(analysis, analysis_issues_sort_order)

            return analysis

        except Exception as error:
            print('Error executing name analysis: ' + repr(error))
            raise

    '''
    do_analysis is an abstract method inherited from NameAnalysisDirector must be implemented.
    This is the main execution call for running name analysis checks.
    @:return ProcedureResult[]
    '''

    def do_analysis(self):
        results = []
        auto_analyze_config = current_app.config.get('AUTO_ANALYZE_CONFIG')

        if auto_analyze_config in ('WELL_FORMED_NAME', 'EXACT_MATCH', 'SEARCH_CONFLICTS'):
            builder = self.builder
            np_svc = self._name_processing_service
            stop_words_list = np_svc.get_stop_words()

            self._get_designations(request_types)

            # Return any combination of these checks
            if not self.skip_search_conflicts and auto_analyze_config in ('EXACT_MATCH', 'SEARCH_CONFLICTS'):
                check_conflicts = builder.search_exact_match(self.get_list_dist(), self.get_list_desc(),
                                                             self.compound_descriptive_name_tokens,
                                                             False, self.get_designation_end_list_all(),
                                                             self.get_designation_any_list_all(), stop_words_list)

                if check_conflicts.is_valid and auto_analyze_config in 'SEARCH_CONFLICTS':
                    check_conflicts = builder.search_conflicts(
                        [self.get_list_dist_search_conflicts()],
                        [self.get_list_desc_search_conflicts()],
                        [self.get_list_desc()],
                        self.name_tokens,
                        self.processed_name,
                        np_svc.get_stand_alone_words()
                    )

                if not check_conflicts.is_valid:
                    results.append(check_conflicts)

            # check_conflicts_queue = builder.search_exact_match(self.get_list_dist(), self.get_list_desc(),
            #                                                    self.compound_descriptive_name_tokens,
            #                                                    True, self.get_designation_end_list_all(),
            #                                                    self.get_designation_any_list_all(), stop_words_list)

            # if check_conflicts_queue.is_valid:
            # check_conflicts_queue = builder.search_conflicts(
            #     [self.get_list_dist_search_conflicts()],
            #     [self.get_list_desc_search_conflicts()],
            #     [self.get_list_desc()],
            #     self.name_tokens,
            #     self.processed_name,
            #     np_svc.get_stand_alone_words(),
            #     check_name_is_well_formed=False,
            #     queue=True
            # )
            #
            # if not check_conflicts_queue.is_valid:
            #     results.append(check_conflicts_queue)

            # TODO: Use the list_name array, don't use a string in the method!
            # check_words_requiring_consent = builder.check_words_requiring_consent(list_name)  # This is correct
            check_words_requiring_consent = builder.check_words_requiring_consent(
                self.name_tokens, self.processed_name
            )

            if not check_words_requiring_consent.is_valid:
                results.append(check_words_requiring_consent)

            # We don't need to check for designations, so we're skipping that here...

            check_special_words = builder.check_word_special_use(self.name_tokens, self.get_processed_name())

            if not check_special_words.is_valid:
                results.append(check_special_words)

        return results
