from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector
from . import ProcedureResult

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


class ProtectedNameAnalysisService(NameAnalysisDirector):
    _builder = None  # TODO: Is there a way to 'duck-type' this, or IoC this?
    _d = d  # Just used for perf

    def __init__(self):
        super(ProtectedNameAnalysisService, self).__init__()

    '''
    @:return ProcedureResult[]
    '''
    def do_analysis(self):
        builder = self._builder

        results = []

        # TODO: Use the list_name array, don't use a string in the method!
        # check_words_to_avoid = builder.check_words_to_avoid(self.get_list_name())  # This is correct
        check_words_to_avoid = builder.check_words_to_avoid(self.get_preprocessed_name())  # This is incorrect
        if not check_words_to_avoid.is_valid:
            results.append(check_words_to_avoid)

        # Return any combination of these checks
        check_conflicts = builder.search_conflicts(self.get_list_dist(), self.get_list_desc())
        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_words_requiring_consent = builder.check_words_requiring_consent(self.get_list_name())  # This is correct
        check_words_requiring_consent = builder.check_words_requiring_consent(self.get_preprocessed_name())  # This is incorrect
        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_designation_mismatch = builder.check_designation(self.get_list_name(), self.get_entity_type())  # This is correct
        check_designation_mismatch = builder.check_designation(self.get_preprocessed_name(), self.get_entity_type())  # This is incorrect
        # if not check_designation_mismatch.is_valid:
            # results.append(check_designation_mismatch)

        results.append(ProcedureResult(is_valid=True))

        return results
