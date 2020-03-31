import re
import collections

from namex.constants import \
    BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes

from namex.services.name_request.auto_analyse.name_analysis_utils import get_flat_list

from . import SynonymServiceMixin
from .. import DesignationPositionCodes


class SynonymDesignationMixin(SynonymServiceMixin):
    def get_designated_end_all_words(self):
        return self.get_designations(None, DesignationPositionCodes.END, 'english')

    def get_designated_any_all_words(self):
        return self.get_designations(None, DesignationPositionCodes.ANY, 'english')

    def get_misplaced_end_designations(self, name, designation_end_entity_type):
        # en_designation_end_all_list = self.get_designations(None, DesignationPositionCodes.END, 'english')
        if not designation_end_entity_type:
            return list()
        designation_any_rgx = '(' + '|'.join(map(str, designation_end_entity_type)) + ')'
        designation_any_regex = r'\b{}\s'.format(designation_any_rgx)

        # Returns list of tuples
        misplaced_designation_any_list = re.findall(designation_any_regex, name.lower())

        return misplaced_designation_any_list

    def get_entity_type_end_designation(self, entity_end_designation_dict, all_designation_any_end_list):
        entity_type_end_designation_name = list()
        for designation_end in all_designation_any_end_list:
            entity_type_end_designation_name.extend(
                self.get_entity_type_by_value(entity_end_designation_dict, designation_end))

        all_entity_types = [item for item, count in collections.Counter(entity_type_end_designation_name).items() if
                            count > 1]

        if all_entity_types:
            return all_entity_types

        return entity_type_end_designation_name

    def get_entity_type_any_designation(self, entity_any_designation_dict, all_designation_any_end_list):
        entity_type_any_designation_name = list()

        for designation_any in all_designation_any_end_list:
            entity_type_any_designation_name.extend(
                self.get_entity_type_by_value(entity_any_designation_dict, designation_any))

        all_entity_types = [item for item, count in collections.Counter(entity_type_any_designation_name).items() if
                            count > 1]

        if all_entity_types:
            return all_entity_types

        return entity_type_any_designation_name

    '''
    Get designations with <end> position for any entity type. This omits the general designation with <end> position:
    English Designations_end Stop
    '''

    def get_designation_end_in_name(self, name):
        en_designation_end_all_list = self.get_designations(None, DesignationPositionCodes.END, 'english')
        designation_end_rgx = '(' + '|'.join(map(str, en_designation_end_all_list)) + ')'
        designation_end_regex = r'{0}(?=(\s{0})*$)'.format(designation_end_rgx)

        # Returns list of tuples
        found_designation_end = re.findall(designation_end_regex, name.lower())

        # Getting list of lists where the first list contains designations of type "anywhere" and the second list contains designations of type "end".
        # [['association],['limited partnership']
        designation_end_list = [list(elem) for elem in found_designation_end]
        if any(isinstance(el, list) for el in designation_end_list):
            designation_end_list = get_flat_list(designation_end_list)
        designation_end_list = list(filter(None, designation_end_list))
        designation_end_list = list(dict.fromkeys(designation_end_list))

        return designation_end_list

    '''
    Get designations with <end> position for any entity type which have incorrect position different to <end>.
    Designations in <end> position which are at the beginning, middle or before <end> position, these designations
    have to be shown as misplaced.
    '''

    def get_incorrect_designation_end_in_name(self, name):
        en_designation_end_all_list = self.get_designations(None, DesignationPositionCodes.END, 'english')
        designation_end_rgx = '|'.join(map(str, en_designation_end_all_list))
        designation_end_regex = r'({})(?=(?:.*\s\w+$))'.format(designation_end_rgx)

        # Returns list of tuples
        found_incorrect_designation_end = re.findall(designation_end_regex, name.lower())

        return found_incorrect_designation_end

    '''
    Get designations with <any> position for any entity type. This omits the general designation with <any> position:
    English Designations_any Stop
    '''

    def get_designation_any_in_name(self, name):
        en_designation_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY, 'english')
        designation_any_rgx = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
        designation_any_regex = r'{}(?=\s|$)'.format(designation_any_rgx)

        # Returns list of tuples
        found_designation_any = re.findall(designation_any_regex, name.lower())

        return found_designation_any

    def get_all_end_designations(self):
        # TODO: Fix RLC we don't have that entity type, code changed to RLC from something else...
        # 'RLC': self._model.get_en_RLC_entity_type_end_designation()
        entity_types = [
            XproUnprotectedNameEntityTypes.XPRO_LIMITED_LIABILITY_COMPANY,
            BCUnprotectedNameEntityTypes.BC_LIMITED_LIABILITY_PARTNERSHIP,
            BCProtectedNameEntityTypes.BC_UNLIMITED_LIABILITY_COMPANY,
            BCProtectedNameEntityTypes.BC_CORPORATION
        ]

        entity_end_designation_dict = {}

        for entity_type in entity_types:
            # TODO: Use an enum for languages too!
            entity_end_designation_dict[entity_type.value] = self.get_designations(
                entity_type,
                DesignationPositionCodes.END,
                'english'
            )

        return entity_end_designation_dict

    def get_all_any_designations(self):
        entity_types = [

        ]

        entity_any_designation_dict = {}

        for entity_type in entity_types:
            # TODO: Use an enum for languages too!
            entity_any_designation_dict[entity_type.value] = self.get_designations(
                entity_type,
                DesignationPositionCodes.ANY,
                'english'
            )

        return entity_any_designation_dict

    def get_entity_type_by_value(self, entity_type_dicts, designation):
        entity_list = list()
        entity__designation_end_list = entity_type_dicts.items()
        print(entity__designation_end_list)
        for entity_designation in entity__designation_end_list:
            if any(designation in value for value in entity_designation[1]):
                entity_list.append(entity_designation[0])
        return entity_list
