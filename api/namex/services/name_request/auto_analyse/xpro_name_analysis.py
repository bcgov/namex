from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector

from .mixins.set_designation_lists import SetDesignationsListsMixin

from . import AnalysisIssueCodes
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

            analysis = []

            # Configure the analysis for the supplied builder
            #self.configure_analysis()
            get_classification(self, syn_svc, self.name_tokens, wc_svc, token_svc)

            check_words_to_avoid = builder.check_words_to_avoid(self.name_tokens, self.processed_name)
            if not check_words_to_avoid.is_valid:
                analysis.append(check_words_to_avoid)
                return analysis

            # Normally we'd do the check_name_is_well_formed analysis here... skip it for extra-provincial names

            check_word_limit = builder.check_word_limit(self.name_tokens)
            if not check_word_limit.is_valid:
                analysis.append(check_word_limit)
                return analysis

            check_word_unclassified = builder.check_unclassified_words(self.name_tokens, self.get_list_none())
            if not check_word_unclassified.is_valid:
                analysis.append(check_word_unclassified)

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
                AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD,
                AnalysisIssueCodes.WORD_SPECIAL_USE,
                AnalysisIssueCodes.NAME_REQUIRES_CONSENT,
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
        builder = self.builder

        results = []

        # Return any combination of these checks
        check_conflicts = builder.search_conflicts(
            [self.get_list_dist()],
            [self.get_list_desc()],
            self.name_tokens,
            self.processed_name
        )

        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        check_conflicts_queue = builder.search_conflicts(
            [self.get_list_dist()],
            [self.get_list_desc()],
            self.name_tokens,
            self.processed_name,
            False,
            True
        )

        if not check_conflicts_queue.is_valid:
            results.append(check_conflicts_queue)

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
