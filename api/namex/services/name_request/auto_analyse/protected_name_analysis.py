from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector

'''
The ProtectedNameAnalysisService returns an analysis response using the strategies in analysis_strategies.py
The response cases are as follows:
- API Returns
- Requires addition of distinctive word
- Requires addition of descriptive word
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


class ProcedureResult:
    def __init__(self, **kwargs):
        self.is_valid = kwargs.get('is_valid', False)
        self.result_code = kwargs.get('result_code', None)


class ProtectedNameAnalysisService(NameAnalysisDirector):
    _builder = None  # TODO: Is there a way to 'duck-type' this, or IoC this?
    _d = d  # Just used for perf

    def __init__(self):
        super(ProtectedNameAnalysisService, self).__init__()

    # Prepare any data required by the analysis builder
    def prepare_data(self):
        # Query database for synonyms, substitutions and designations
        synonyms = self._synonyms_api.get_synonyms()
        substitutions = self._synonyms_api.get_substitutions()

        stop_words = self._synonyms_api.get_stop_words()
        designated_end_words = self._synonyms_api.get_designated_end_words()
        designated_any_words = self._synonyms_api.get_designated_any_words()

        # Solr calls
        in_province_conflicts = self._solr_api.get_in_province_conflicts()
        all_conflicts = self._solr_api.get_all_conflicts()

        # Store query results to instance
        self._synonyms = synonyms
        self._substitutions = substitutions

        self._stop_words = stop_words  # stop_words['synonyms_text'][0].split(',')
        self._designated_end_words = designated_end_words  # designated_end_words['synonyms_text'][0].split(',')
        self._designated_any_words = designated_any_words  # designated_any_words['synonyms_text'][0].split(',')

        self._in_province_conflicts = in_province_conflicts
        self._all_conflicts = all_conflicts

        self._builder.set_dicts(
            synonyms=self._synonyms,
            substitutions=self._substitutions,
            stop_words=self._stop_words,
            designated_end_words=self._designated_end_words,
            designated_any_words=self._designated_any_words,
            in_province_conflicts=self._in_province_conflicts,
            all_conflicts=self._all_conflicts
        )

    '''
    This is the main execution call for the class
    @:return ProcedureResult[]
    '''
    def execute_analysis(self):
        builder = self._builder

        check_name_is_well_formed = builder.check_name_is_well_formed(builder.get_list_dist(), builder.get_list_desc(), builder.get_list_none(), builder.get_list_name())
        check_words_to_avoid = builder.check_words_to_avoid()
        check_conflicts = builder.search_conflicts(builder.get_list_dist(), builder.get_list_desc())
        check_words_requiring_consent = builder.check_words_requiring_consent()
        check_designation_mismatch = builder.check_designation()

        results = []

        if not check_name_is_well_formed.is_valid:
            results.append(check_name_is_well_formed)
            return results
            #  Do not continue

        if not check_words_to_avoid.is_valid:
            results.append(check_words_to_avoid)
            return results
            #  Do not continue

        # Return any combination of these checks
        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        if not check_designation_mismatch.is_valid:
            results.append(check_designation_mismatch)

        results.append(ProcedureResult(is_valid=True))

        return results
