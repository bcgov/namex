from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector
import pandas as pd

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

    '''
    This is the main execution call for the class
    @:return ProcedureResult[]
    '''
    def do_analysis(self):
        builder = self._builder

        results = []

        check_words_to_avoid = builder.check_words_to_avoid(self.get_list_name())
        if not check_words_to_avoid.is_valid:
            results.append(check_words_to_avoid)
            return results
            #  Do not continue

        # Return any combination of these checks
        check_conflicts = builder.search_conflicts(self.get_list_dist(), self.get_list_desc())
        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        check_words_requiring_consent = builder.check_words_requiring_consent()
        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        check_designation_mismatch = builder.check_designation()
        if not check_designation_mismatch.is_valid:
            results.append(check_designation_mismatch)

        results.append(ProcedureResult(is_valid=True))

        return results
