from datetime import (datetime)

from .name_analysis_director import NameAnalysisDirector
from . import ProcedureResult

from .name_analysis_utils import words_distinctive_descriptive

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

        check_words_to_avoid = builder.check_words_to_avoid(self.get_list_name(), self.get_preprocessed_name())
        if not check_words_to_avoid.is_valid:
            results.append(check_words_to_avoid)

        # Check if list_dist and list_desc are the same
        if self.get_list_dist() == self.get_list_desc():
            self._list_dist_words, self._list_desc_words = words_distinctive_descriptive(self.get_list_name())
        else:
            lst_dist = []
            lst_desc = []
            lst_dist.append(self._list_dist_words)
            lst_desc.append(self._list_desc_words)

            self._list_dist_words = lst_dist
            self._list_desc_words = lst_desc

        # Return any combination of these checks
        check_conflicts = builder.search_conflicts(self.get_list_dist(), self.get_list_desc())
        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_words_requiring_consent = builder.check_words_requiring_consent(self.get_list_name())  # This is correct
        check_words_requiring_consent = builder.check_words_requiring_consent(
            self.get_list_name(), self.get_preprocessed_name())  # This is incorrect
        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_designation_mismatch = builder.check_designation(self.get_list_name(), self.get_entity_type())  # This is correct
        self.set_designations_by_entity_type_user(
            self.get_entity_type())  # Set _designation_any_list_user and _designation_end_list_user based on entity type typed by user
        self.set_designations_by_input_name(
            self.get_preprocessed_name())  # Set _designation_any_list and _designation_end_list based on company name typed by user
        self.set_wrong_designation_by_input_name(
            self.get_preprocessed_name())  # Set _wrong_designation_place based on company name typed by user
        self.set_entity_type_any_designation(self._entity_any_designation_dict,
                                             self._designation_any_list)  # Set _entity_type_any_designation for designations based on
        # company name typed by user
        self.set_entity_type_end_designation(self._entity_end_designation_dict,
                                             self._designation_end_list)  # Set _entity_type_end_designation for designations based on
        # company name typed by user
        self.set_all_designations_user()  # Set all designations based on entity type typed by user
        self.set_all_designations()  # Set all designations based on company name typed by user
        check_designation_mismatch = builder.check_designation(self.get_list_name(),
                                                               self.get_entity_type(),
                                                               self.get_all_designations(),
                                                               self.get_wrong_designation_by_input_name(),
                                                               self.get_all_designations_user())
        check_special_words = builder.check_word_special_use(self.get_list_name(), self.get_name())

        if not check_designation_mismatch.is_valid:
            results.append(check_designation_mismatch)
        if not check_special_words.is_valid:
            results.append(check_special_words)
        # else:
        #    results.append(ProcedureResult(is_valid=True))

        return results
