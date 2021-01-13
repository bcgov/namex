from namex.constants import \
    BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes, \
    DesignationPositionCodes, LanguageCodes

from namex.utils.common import parse_dict_of_lists


class SetDesignationsListsMixin(object):
    def _set_designations(self):
        # Set available designations for entity type selected by user (by default designations related to 'CR' entity type)
        # _designation_any_list_correct and_designation_end_list_correct contain only correct designations in English and French
        self._set_designations_by_entity_type_user()

        # Set _designation_any_list and _designation_end_list are only correct designations based on company name typed by user
        # Set _all_designations contains all found designations in company name typed by user
        self._set_designations_by_input_name()

        # Set _misplaced_designation_end_list which contains <end> designations in other part of the name
        self._set_designations_incorrect_position_by_input_name()

        # Set _entity_type_any_designation for designations found on company name typed by user
        self._set_entity_type_any_designation()

        # Set _entity_type_end_designation for designations found on company name typed by user
        self._set_entity_type_end_designation()

        # Set all designations based on entity type typed by user,'CR' by default
        self._all_designations_user = self._eng_designation_all_list_correct + self._fr_designation_all_list_correct

    '''
    Set the corresponding entity type for designations <any> found in name
    '''

    def _set_entity_type_any_designation(self):
        syn_svc = self.synonym_service
        designation_any_list = self._designation_any_list

        all_any_designations = syn_svc.get_all_any_designations()

        self._entity_type_any_designation = syn_svc.get_entity_type_any_designation(
            entity_any_designation_dict=parse_dict_of_lists(all_any_designations),
            all_designation_any_end_list=designation_any_list
        )

    '''
    Set the corresponding entity type for designations <end> found in name
    '''

    def _set_entity_type_end_designation(self):
        syn_svc = self.synonym_service
        designation_end_list = self._designation_end_list

        all_end_designations = syn_svc.get_all_end_designations()

        self._entity_type_end_designation = syn_svc.get_entity_type_end_designation(
            entity_end_designation_dict=parse_dict_of_lists(all_end_designations),
            all_designation_any_end_list=designation_end_list
        )

    def _set_designations_by_entity_type_user(self):
        syn_svc = self.synonym_service
        entity_type = self.entity_type

        entity_type_code = None
        if BCProtectedNameEntityTypes.has_value(entity_type) and BCProtectedNameEntityTypes(entity_type):
            entity_type_code = BCProtectedNameEntityTypes(entity_type)
        elif BCUnprotectedNameEntityTypes.has_value(entity_type) and BCUnprotectedNameEntityTypes(entity_type):
            entity_type_code = BCUnprotectedNameEntityTypes(entity_type)
        elif XproUnprotectedNameEntityTypes.has_value(entity_type) and XproUnprotectedNameEntityTypes(entity_type):
            entity_type_code = XproUnprotectedNameEntityTypes(entity_type)
        else:
            raise Exception(
                'Could not set entity type user designations - entity type [' + entity_type + '] was not found in BC or XPRO entity types!')

        self._eng_designation_any_list_correct = syn_svc.get_designations(entity_type_str=entity_type_code.value,
                                                                          position_str=DesignationPositionCodes.ANY.value,
                                                                          lang=LanguageCodes.ENG.value)

        self._eng_designation_end_list_correct = syn_svc.get_designations(entity_type_str=entity_type_code.value,
                                                                          position_str=DesignationPositionCodes.END.value,
                                                                          lang=LanguageCodes.ENG.value)

        self._fr_designation_any_list_correct = syn_svc.get_designations(entity_type_str=entity_type_code.value,
                                                                         position_str=DesignationPositionCodes.ANY.value,
                                                                         lang=LanguageCodes.FR.value)

        self._fr_designation_end_list_correct = syn_svc.get_designations(entity_type_str=entity_type_code.value,
                                                                         position_str=DesignationPositionCodes.END.value,
                                                                         lang=LanguageCodes.FR.value)

        self._eng_designation_all_list_correct = self._eng_designation_any_list_correct + self._eng_designation_end_list_correct
        self._eng_designation_all_list_correct.sort(key=len, reverse=True)

        self._fr_designation_all_list_correct = self._fr_designation_any_list_correct + self._fr_designation_end_list_correct
        self._fr_designation_all_list_correct.sort(key=len, reverse=True)

        self._designation_any_list_correct = self._eng_designation_any_list_correct + self._fr_designation_any_list_correct
        self._designation_any_list_correct.sort(key=len, reverse=True)

        self._designation_end_list_correct = self._eng_designation_end_list_correct + self._fr_designation_end_list_correct
        self._designation_end_list_correct.sort(key=len, reverse=True)

    '''
    Set designations in <any> and <end> positions regardless the entity type. 
    designation_any_list: Retrieves all designations properly placed anywhere in the name regardless the entity type.
                           <Entity type>-Valid English Designations_any Stop
                           English Designations_any Stop.
    designation_end_list: Retrieves all designations properly placed at the end in the name regardless the entity type
                           <Entity type>-Valid English Designations_end Stop
                           English Designations_end Stop.
    all_designations: Retrieves all designations in company name.
    '''

    def _set_designations_by_input_name(self):
        syn_svc = self.synonym_service
        np_svc = self.name_processing_service

        # Get the first section of name when exists slash. For instance, ARMSTRONG PLUMBING LTD./ ARMSTRONG PLUMBING LIMITEE
        # Just take ARMSTRONG PLUMBING LTD. and perform analysis of designations.
        name_first_part = np_svc.name_first_part

        self._designation_any_list = syn_svc.get_designation_any_in_name(name=name_first_part)
        self._designation_end_list = syn_svc.get_designation_end_in_name(name=name_first_part)

        self._all_designations = syn_svc.get_designation_all_in_name(name=name_first_part)

    '''
    Set designations in position <end> found any other place in the company name, these designations are misplaced.
    '''

    def _set_designations_incorrect_position_by_input_name(self):
        syn_svc = self.synonym_service
        tokenized_name = self.get_original_name_tokenized()
        correct_designation_end_list = self._designation_end_list_correct

        designation_end_misplaced_list = syn_svc.get_incorrect_designation_end_in_name(tokenized_name=tokenized_name,
                                                                                       designation_end_entity_type=correct_designation_end_list)
        self._misplaced_designation_end_list = designation_end_misplaced_list

    def _get_designations(self, request_type_list_dict):
        syn_svc = self.synonym_service

        for key, value in request_type_list_dict.items():
            if DesignationPositionCodes.END.value in value:
                self._designation_end_list_all.extend(syn_svc.get_designations(entity_type_str=key,
                                                                               position_str=DesignationPositionCodes.END.value,
                                                                               lang=LanguageCodes.ENG.value))
                self._designation_end_list_all.extend(syn_svc.get_designations(entity_type_str=key,
                                                                               position_str=DesignationPositionCodes.END.value,
                                                                               lang=LanguageCodes.FR.value))
            if DesignationPositionCodes.ANY.value in value:
                self._designation_any_list_all.extend(syn_svc.get_designations(entity_type_str=key,
                                                                               position_str=DesignationPositionCodes.ANY.value,
                                                                               lang=LanguageCodes.ENG.value))
                self._designation_any_list_all.extend(syn_svc.get_designations(entity_type_str=key,
                                                                               position_str=DesignationPositionCodes.ANY.value,
                                                                               lang=LanguageCodes.FR.value))

        self._designation_end_list_all = sorted(set(self._designation_end_list_all), key=len, reverse=True)
        self._designation_any_list_all = sorted(set(self._designation_any_list_all), key=len, reverse=True)
