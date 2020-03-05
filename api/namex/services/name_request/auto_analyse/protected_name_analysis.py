from datetime import (datetime)

import collections

from namex.constants import \
    BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes

from namex.services.synonyms import DesignationPositionCodes

from .name_analysis_director import NameAnalysisDirector
from . import ProcedureResult

from .name_analysis_utils import list_distinctive_descriptive_same, validate_distinctive_descriptive_lists, \
    list_distinctive_descriptive

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
    _d = d  # Just used for perf

    def __init__(self):
        super(ProtectedNameAnalysisService, self).__init__()

    def _set_designations_by_input_name(self):
        syn_svc = self.synonym_service
        original_name = self.get_original_name()

        self._designation_any_list = syn_svc.get_designation_any_in_name(original_name)
        self._designation_end_list = syn_svc.get_designation_end_in_name(original_name)

    def _set_wrong_designation_by_input_name(self):
        syn_svc = self.synonym_service
        original_name = self.get_original_name()

        self._wrong_designation_any_list = syn_svc.get_wrong_place_any_designations(original_name)
        self._wrong_designation_end_list = syn_svc.get_wrong_place_end_designations(original_name)

        self._wrong_designation_place = self._wrong_designation_any_list + self._wrong_designation_end_list

    # TODO: I don't see this called anywhere (was prev called: set_all_entity_types)
    def _set_all_entity_types(self):
        self._all_entity_types = [item for item, count in collections.Counter(
            self._entity_type_any_designation + self._entity_type_end_designation
        ).items() if count > 1]

        if not self._all_entity_types:
            self._all_entity_types = self._entity_type_any_designation + self._entity_type_end_designation

    def _set_designations_by_entity_type_user(self):
        syn_svc = self.synonym_service
        entity_type = self.entity_type

        entity_type_code = None
        if BCProtectedNameEntityTypes(entity_type):
            entity_type_code = BCProtectedNameEntityTypes(entity_type)
        elif BCUnprotectedNameEntityTypes(entity_type):
            entity_type_code = BCUnprotectedNameEntityTypes(entity_type)
        elif XproUnprotectedNameEntityTypes(entity_type):
            entity_type_code = XproUnprotectedNameEntityTypes(entity_type)

        any_list = syn_svc.get_designations(entity_type_code, DesignationPositionCodes.ANY, 'english')
        end_list = syn_svc.get_designations(entity_type_code, DesignationPositionCodes.END, 'english')

        self._designation_any_list_user.extend(any_list)
        self._designation_end_list_user.extend(end_list)

    def _set_entity_type_any_designation(self):
        syn_svc = self.synonym_service
        entity_any_designation_dict = self._entity_any_designation_dict
        designation_any_list = self._designation_any_list

        self._entity_type_any_designation = syn_svc.get_entity_type_any_designation(
            syn_svc.get_all_end_designations(), designation_any_list
        )

    def _set_entity_type_end_designation(self):
        syn_svc = self.synonym_service
        entity_end_designation_dict = self._entity_end_designation_dict
        designation_end_list = self._designation_end_list

        self._entity_type_end_designation = syn_svc.get_entity_type_end_designation(
            syn_svc.get_all_any_designations(), designation_end_list
        )

    def _set_designations(self):
        self._set_designations_by_entity_type_user()
        # Set _designation_any_list and _designation_end_list based on company name typed by user
        self._set_designations_by_input_name()
        # Set _wrong_designation_place based on company name typed by user
        self._set_wrong_designation_by_input_name()
        # TODO: Double check this to make sure it works
        # Set _entity_type_any_designation for designations based on company name typed by user
        self._set_entity_type_any_designation()
        # TODO: Double check this to make sure it works
        # Set _entity_type_end_designation for designations based on company name typed by user
        self._set_entity_type_end_designation()

        # Set all designations based on entity type typed by user
        self._all_designations_user = self._designation_any_list_user + self._designation_end_list_user
        # Set all designations based on company name typed by user
        self._all_designations = self._designation_any_list + self._designation_end_list

    '''
    do_analysis is an abstract method inherited from NameAnalysisDirector must be implemented.
    This is the main execution call for running name analysis checks.
    @:return ProcedureResult[]
    '''

    def do_analysis(self):
        builder = self.builder

        list_name = self.name_tokens
        list_dist, list_desc, list_none = self.word_classification_tokens

        results = []

        check_words_to_avoid = builder.check_words_to_avoid(list_name, self.processed_name)
        if not check_words_to_avoid.is_valid:
            results.append(check_words_to_avoid)
            return results
            #  Do not continue

        if self.token_classifier.distinctive_word_tokens == self.token_classifier.descriptive_word_tokens:
            self._list_dist_words, self._list_desc_words = list_distinctive_descriptive_same(self.name_tokens)

        else:
            self._list_dist_words, self._list_desc_words = list_distinctive_descriptive(self.name_tokens,
                                                                                        self.token_classifier.distinctive_word_tokens,
                                                                                        self.token_classifier.descriptive_word_tokens)

        # Return any combination of these checks
        check_conflicts = builder.search_conflicts(self._list_dist_words, self._list_desc_words, self.name_tokens,
                                                   self.processed_name)

        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_words_requiring_consent = builder.check_words_requiring_consent(list_name)  # This is correct
        check_words_requiring_consent = builder.check_words_requiring_consent(
            self.name_tokens, self.processed_name)  # This is incorrect

        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        # Set designations and run our check
        self._set_designations()

        check_designation_mismatch = builder.check_designation(
            self.get_original_name().lower().split(),
            self.entity_type,
            self.get_all_designations(),
            self.get_wrong_designation_by_input_name(),
            self.get_all_designations_user()
        )

        if not check_designation_mismatch.is_valid:
            results.append(check_designation_mismatch)

        check_special_words = builder.check_word_special_use(self.name_tokens, self.get_original_name())

        if not check_special_words.is_valid:
            results.append(check_special_words)

        # DO NOT GET RID OF THIS! WE EXPLICITLY NEED TO RETURN A VALID ProcedureResult!
        if not results.__len__() > 0:
            results.append(ProcedureResult(is_valid=True))

        return results
