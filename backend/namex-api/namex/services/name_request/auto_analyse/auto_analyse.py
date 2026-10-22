# !!!!! DEPRECATED !!!! This is just in here so it's easier to merge, we'll delete when we are done

from datetime import datetime

from .name_analysis_director import NameAnalysisDirector

"""
The AutoAnalyseService returns an analysis response using the strategies in analysis_strategies.py
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
"""

d = datetime.now()  # Was just used for perf analysis


class AutoAnalyseService(NameAnalysisDirector):
    _builder = None  # TODO: Is there a way to 'duck-type' this, or IoC this?
    _d = d  # Just used for perf

    def __init__(self):
        super(AutoAnalyseService, self).__init__()
