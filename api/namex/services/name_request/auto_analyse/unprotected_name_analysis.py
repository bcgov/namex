from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector

'''
The UnprotectedNameAnalysisService returns an analysis response using the strategies in analysis_strategies.py
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


class UnprotectedNameAnalysisService(NameAnalysisDirector):
    _builder = None  # TODO: Is there a way to 'duck-type' this, or IoC this?
    _d = d  # Just used for perf

    def __init__(self):
        super(UnprotectedNameAnalysisService, self).__init__()

    '''
    This is the main execution call for the class
    @:return ProcedureResult[]
    '''
    def do_analysis(self):
        builder = self._builder

        # TODO: If XPRO then run unclassified word check too
        check_conflicts = builder.search_conflicts(builder.get_list_dist(), builder.get_list_desc())

        results = []

        if not check_conflicts.is_valid:
            results.append(check_conflicts)
            return results

        return ProcedureResult(is_valid=True)




