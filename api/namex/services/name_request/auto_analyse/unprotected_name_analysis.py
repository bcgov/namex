import collections
import os
from datetime import datetime

from flask import current_app

from namex.constants import (
    BCProtectedNameEntityTypes,
    BCUnprotectedNameEntityTypes,
    DesignationPositionCodes,
    LanguageCodes,
    XproUnprotectedNameEntityTypes,
)
from namex.utils.common import parse_dict_of_lists

from . import ProcedureResult
from .name_analysis_director import NameAnalysisDirector


"""
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
"""

d = datetime.now()  # Was just used for perf analysis


class UnprotectedNameAnalysisService(NameAnalysisDirector):
    # _builder = None  # TODO: Is there a way to 'duck-type' this, or IoC this?
    _d = d  # Just used for perf

    def __init__(self):
        super(UnprotectedNameAnalysisService, self).__init__()

    def _set_designations_by_input_name(self):
        syn_svc = self.synonym_service
        original_name = self.get_original_name()

        # designation any/end_list get the designation at any/end place as long as they are placed correctly:
        designation_any_list = syn_svc.get_designation_any_in_name(name=original_name).data
        designation_end_list = syn_svc.get_designation_end_in_name(name=original_name).data

        # all_designations gets all the designations regardless they are placed correctly or not.
        # For instance, if limited liability partnership (end designation) is placed in a different location then
        # we will get the designation in here, but not in the previous lists (designation any/end list)
        all_designations = syn_svc.get_designation_all_in_name(name=original_name).data

        for idx, designation in enumerate(designation_any_list):
            if not designation in all_designations:
                designation_any_list.pop(idx)

        for idx, designation in enumerate(designation_end_list):
            if not designation in all_designations:
                designation_end_list.pop(idx)

        self._designation_any_list = designation_any_list
        self._designation_end_list = designation_end_list
        self._all_designations = all_designations

    def _set_misplaced_designation_in_input_name(self):
        syn_svc = self.synonym_service
        original_name = self.get_original_name()
        correct_designation_end = self._designation_end_list_correct
        correct_designation_any = self._designation_any_list_correct
        self._misplaced_designation_any_list = syn_svc.get_misplaced_any_designations(
            name=original_name, designation_any_entity_type=correct_designation_any
        ).data
        self._misplaced_designation_end_list = syn_svc.get_misplaced_end_designations(
            name=original_name, designation_end_entity_type=correct_designation_end
        ).data

        self._misplaced_designation_all_list = (
            self._misplaced_designation_any_list + self._misplaced_designation_end_list
        )

    # TODO: I don't see this called anywhere (was prev called: set_all_entity_types)
    def _set_all_entity_types(self):
        self._all_entity_types = [
            item
            for item, count in collections.Counter(
                self._entity_type_any_designation + self._entity_type_end_designation
            ).items()
            if count > 1
        ]

        if not self._all_entity_types:
            self._all_entity_types = self._entity_type_any_designation + self._entity_type_end_designation

    def _set_designations_by_entity_type_user(self):
        syn_svc = self.synonym_service
        entity_type = self.entity_type

        entity_type_code = None
        if BCProtectedNameEntityTypes.has_value(entity_type):
            entity_type_code = BCProtectedNameEntityTypes(entity_type)
        elif BCUnprotectedNameEntityTypes.has_value(entity_type):
            entity_type_code = BCUnprotectedNameEntityTypes(entity_type)
        elif XproUnprotectedNameEntityTypes.has_value(entity_type):
            entity_type_code = XproUnprotectedNameEntityTypes(entity_type)

        any_list = syn_svc.get_designations(
            entity_type_code=entity_type_code.value,
            position_code=DesignationPositionCodes.ANY.value,
            lang=LanguageCodes.ENG.value,
        ).data

        end_list = syn_svc.get_designations(
            entity_type_code=entity_type_code.value,
            position_code=DesignationPositionCodes.END.value,
            lang=LanguageCodes.ENG.value,
        ).data

        self._designation_any_list_correct.extend(any_list)
        self._designation_end_list_correct.extend(end_list)

    def _set_entity_type_any_designation(self):
        syn_svc = self.synonym_service
        designation_any_list = self._designation_any_list

        designations = syn_svc.get_all_end_designations().data
        designations_dict = parse_dict_of_lists(designations)

        self._entity_type_any_designation = syn_svc.get_entity_type_any_designation(
            entity_any_designation_dict=designations_dict, all_designation_any_end_list=designation_any_list
        ).data

    def _set_entity_type_end_designation(self):
        syn_svc = self.synonym_service
        # entity_end_designation_dict = self._entity_end_designation_dict
        designation_end_list = self._designation_end_list

        designations = syn_svc.get_all_any_designations().data
        designations_dict = parse_dict_of_lists(designations)

        self._entity_type_end_designation = syn_svc.get_entity_type_end_designation(
            entity_end_designation_dict=designations_dict, all_designation_any_end_list=designation_end_list
        ).data

    def _set_designations(self):
        self._set_designations_by_entity_type_user()
        # Set _designation_any_list and _designation_end_list based on company name typed by user
        self._set_designations_by_input_name()
        # TODO: Double check this to make sure it works
        # Set _entity_type_any_designation for designations based on company name typed by user
        self._set_entity_type_any_designation()
        # TODO: Double check this to make sure it works
        # Set _entity_type_end_designation for designations based on company name typed by user
        self._set_entity_type_end_designation()
        # Set _misplaced_designation_all based on company name typed by user
        self._set_misplaced_designation_in_input_name()

        # Set all designations based on entity type typed by user
        self._all_designations_user = self._designation_any_list_correct + self._designation_end_list_correct
        # Set all designations based on company name typed by user
        # self._all_designations = self._designation_any_list + self._designation_end_list

    """
    do_analysis is an abstract method inherited from NameAnalysisDirector must be implemented.
    This is the main execution call for running name analysis checks.
    @:return ProcedureResult[]
    """

    def do_analysis(self):
        results = []
        auto_analyze_config = current_app.config.get('AUTO_ANALYZE_CONFIG')

        if auto_analyze_config in ('WELL_FORMED_NAME', 'EXACT_MATCH', 'SEARCH_CONFLICTS'):
            builder = self.builder

            # list_name = self.name_tokens

            # check_words_to_avoid = builder.check_words_to_avoid(list_name, self.processed_name)
            # if not check_words_to_avoid.is_valid:
            #     results.append(check_words_to_avoid)
            #     return results
            #  Do not continue

            # Return any combination of these checks
            # check_conflicts = builder.search_exact_match(self.processed_name, self.name_tokens)

            # if not check_conflicts.is_valid:
            #     results.append(check_conflicts)

            # TODO: Use the list_name array, don't use a string in the method!
            # check_words_requiring_consent = builder.check_words_requiring_consent(list_name)  # This is correct
            # check_words_requiring_consent = builder.check_words_requiring_consent(
            #     self.name_tokens, self.processed_name)  # This is incorrect

            # if not check_words_requiring_consent.is_valid:
            #     results.append(check_words_requiring_consent)

            # Set designations and run our check
            self._set_designations()

            check_designation_mismatch = builder.check_designation_mismatch(
                self.get_original_name_tokenized(),
                self.entity_type,
                self.get_all_designations(),
                self.get_all_designations_user(),
            )

            if not check_designation_mismatch.is_valid:
                results.append(check_designation_mismatch)

            check_designation_misplaced = builder.check_designation_misplaced(
                self.get_original_name_tokenized(),
                self.get_misplaced_designation_any(),
                self.get_misplaced_designation_end(),
                self.get_misplaced_designation_all(),
            )

            if not check_designation_misplaced.is_valid:
                results.append(check_designation_misplaced)

            # check_special_words = builder.check_word_special_use(self.name_tokens, self.get_original_name())

            # if not check_special_words.is_valid:
            #     results.append(check_special_words)

            # DO NOT GET RID OF THIS! WE EXPLICITLY NEED TO RETURN A VALID ProcedureResult!
            if not results.__len__() > 0:
                results.append(ProcedureResult(is_valid=True))

        return results
