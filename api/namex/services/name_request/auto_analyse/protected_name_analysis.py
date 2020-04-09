from datetime import (datetime)

from namex.constants import \
    BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes

from namex.services.synonyms import DesignationPositionCodes, LanguageCodes

from .name_analysis_director import NameAnalysisDirector

from namex.utils.common import parse_dict_of_lists

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

    '''
    Set designations in <any> and <end> positions regardless the entity type. 
    designation_any_list: Retrieves all designations found anywhere in the name regardless the entity type.
                          <Entity type>-Valid English Designations_any Stop
                          English Designations_any Stop
    designation_end_list: Retrieves all designations found at the end in the name regardless the entity type
                          <Entity type>-Valid English Designations_end Stop
                          English Designations_end Stop,
    Note: The previous lists contain designations that are in the correct position. For instance, designations with <end> position 
          found anywhere are not counted here, they are counted in _set_designations_incorrect_position_by_input_name.
    '''

    def _set_designations_by_input_name(self):
        syn_svc = self.synonym_service
        original_name = self.get_original_name()

        designation_any_list = syn_svc.get_designation_any_in_name(name=original_name).data
        designation_end_list = syn_svc.get_designation_end_in_name(name=original_name).data

        self._designation_any_list = designation_any_list
        self._designation_end_list = designation_end_list

        self._all_designations = self._designation_any_list + self._designation_end_list

    '''
    Set designations in position <end> found any other place in the company name, these designations are misplaced.
    '''

    def _set_designations_incorrect_position_by_input_name(self):
        syn_svc = self.synonym_service
        original_name = self.get_original_name()

        designation_end_misplaced_list = syn_svc.get_incorrect_designation_end_in_name(name=original_name).data
        self._misplaced_designation_end_list = designation_end_misplaced_list

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

        any_list = syn_svc.get_designations(entity_type_code=entity_type_code.value, position_code=DesignationPositionCodes.ANY.value, lang=LanguageCodes.ENG.value).data
        end_list = syn_svc.get_designations(entity_type_code=entity_type_code.value, position_code=DesignationPositionCodes.END.value, lang=LanguageCodes.ENG.value).data

        self._designation_any_list_correct = any_list
        self._designation_end_list_correct = end_list

    '''
    Set the corresponding entity type for designations <any> found in name
    '''

    def _set_entity_type_any_designation(self):
        syn_svc = self.synonym_service
        # entity_any_designation_dict = self._entity_any_designation_dict
        designation_any_list = self._designation_any_list

        all_end_designations = syn_svc.get_all_end_designations().data

        self._entity_type_any_designation = syn_svc.get_entity_type_any_designation(
            entity_any_designation_dict=parse_dict_of_lists(all_end_designations),
            all_designation_any_end_list=designation_any_list
        ).data

    '''
    Set the corresponding entity type for designations <end> found in name
    '''

    def _set_entity_type_end_designation(self):
        syn_svc = self.synonym_service
        # entity_end_designation_dict = self._entity_end_designation_dict
        designation_end_list = self._designation_end_list

        all_any_designations = syn_svc.get_all_any_designations().data

        self._entity_type_end_designation = syn_svc.get_entity_type_end_designation(
            entity_end_designation_dict=parse_dict_of_lists(all_any_designations),
            all_designation_any_end_list=designation_end_list
        ).data

    def _set_designations(self):
        # Set available designations for entity type selected by user (by default designations related to 'CR' entity type)
        # _designation_any_list_user and _designation_end_list_user contain the only correct designations
        self._set_designations_by_entity_type_user()

        # Set _designation_any_list and _designation_end_list based on company name typed by user
        # Set _all_designations (general list) based on company name typed by user
        # All previous set designations have correct position, but may belong to wrong entity type
        self._set_designations_by_input_name()

        # Set _misplaced_designation_end_list which contains <end> designations in other part of the name
        self._set_designations_incorrect_position_by_input_name()

        # Set _entity_type_any_designation for designations found on company name typed by user
        self._set_entity_type_any_designation()

        # Set _entity_type_end_designation for designations found on company name typed by user
        self._set_entity_type_end_designation()

        # Set _misplaced_designation_all based on company name typed by user
        # self._set_misplaced_designation_in_input_name()

        # Set all designations based on entity type typed by user,'CR' by default
        self._all_designations_user = self._designation_any_list_correct + self._designation_end_list_correct

        # Set all designations based on company name typed by user
        # self._all_designations = self._designation_any_list + self._designation_end_list

    '''
    do_analysis is an abstract method inherited from NameAnalysisDirector must be implemented.
    This is the main execution call for running name analysis checks.
    @:return ProcedureResult[]
    '''

    def do_analysis(self):
        builder = self.builder

        list_name = self.name_tokens
        # list_dist, list_desc, list_none = self.word_classification_tokens

        results = []

        # Return any combination of these checks
        check_conflicts = builder.search_conflicts(builder.get_list_dist(), builder.get_list_desc(), self.name_tokens,
                                                   self.processed_name)

        if not check_conflicts.is_valid:
            results.append(check_conflicts)

        # TODO: Use the list_name array, don't use a string in the method!
        # check_words_requiring_consent = builder.check_words_requiring_consent(list_name)  # This is correct
        check_words_requiring_consent = builder.check_words_requiring_consent(
            self.name_tokens, self.processed_name
        )

        if not check_words_requiring_consent.is_valid:
            results.append(check_words_requiring_consent)

        # Set designations and run our check
        self._set_designations()

        check_designation_mismatch = builder.check_designation_mismatch(
            self.get_original_name_tokenized(),
            self.entity_type,
            self.get_all_designations(),
            self.get_all_designations_user()
        )

        if not check_designation_mismatch.is_valid:
            results.append(check_designation_mismatch)

        check_designation_misplaced = builder.check_designation_misplaced(
            self.get_original_name_tokenized(),
            self.get_misplaced_designation_end()
        )

        if not check_designation_misplaced.is_valid:
            results.append(check_designation_misplaced)

        return results
