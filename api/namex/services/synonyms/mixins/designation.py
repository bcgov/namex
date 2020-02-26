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

    def get_designation_end_in_name(self, name):
        en_designation_end_all_list = self.get_designations(None, DesignationPositionCodes.END, 'english')
        designation_end_rgx = '(' + '|'.join(map(str, en_designation_end_all_list)) + ')'
        designation_end_regex = r'' + designation_end_rgx + '(?=(\s' + designation_end_rgx + ')*$)'

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

    def get_designation_all_in_name(self, name):
        all_designations_end_all_list = self.get_designations(None, DesignationPositionCodes.END, 'english')
        all_designations_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY, 'english')

        all_designations = list(set(all_designations_end_all_list + all_designations_any_all_list))

        all_designations.sort(key=len, reverse=True)

        all_designations_rgx = '(' + '|'.join(map(str, all_designations)) + ')'
        all_designations_regex = r'' + all_designations_rgx + '(?=\\s|$)'

        # Returns list of tuples
        found_all_designations = re.findall(all_designations_regex, name.lower())

        return found_all_designations

    def get_designation_any_in_name(self, name):
        en_designation_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY, 'english')
        designation_any_rgx = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
        designation_any_regex = designation_any_rgx + '(?=\\s)'

        # Returns list of tuples
        found_designation_any = re.findall(designation_any_regex, name.lower())

        return found_designation_any

    def get_misplaced_any_designations(self, name, designation_any_entity_type):
        # en_designation_any_all_list = self.get_designations(entity_type, DesignationPositionCodes.ANY, 'english')
        if not designation_any_entity_type:
            return list()
        designation_end_rgx = '(' + '|'.join(map(str, designation_any_entity_type)) + ')'
        designation_end_regex = r'' + designation_end_rgx + '(?=(\s' + designation_end_rgx + ')*$)'

        # Returns list of tuples
        found_designation_end = re.findall(designation_end_regex, name.lower())

        # Getting list of lists where the first list contains designations of type "anywhere" and the second list contains designations of type "end".
        # [['association],['limited partnership']
        misplaced_designation_end_list = [list(elem) for elem in found_designation_end]
        if any(isinstance(el, list) for el in misplaced_designation_end_list):
            misplaced_designation_end_list = get_flat_list(misplaced_designation_end_list)
        misplaced_designation_end_list = list(filter(None, misplaced_designation_end_list))
        misplaced_designation_end_list = list(dict.fromkeys(misplaced_designation_end_list))

        return misplaced_designation_end_list

    def get_all_end_designations(self):
        # TODO: Fix RLC we don't have that entity type, code changed to RLC from something else...
        # 'RLC': self._model.get_en_RLC_entity_type_end_designation()
        entity_types = [
            XproUnprotectedNameEntityTypes.XPRO_LIMITED_LIABILITY_COMPANY,
            BCUnprotectedNameEntityTypes.BC_LIMITED_LIABILITY_PARTNERSHIP,
            # TODO: Arturo, if these are commented out, why? Document...
            # BCProtectedNameEntityTypes.BC_COMMUNITY_CONTRIBUTION_COMPANY,
            BCProtectedNameEntityTypes.BC_UNLIMITED_LIABILITY_COMPANY,
            # TODO: Arturo, if these are commented out, why? Document...
            # BCProtectedNameEntityTypes.BC_BENEFIT_COMPANY,
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
            # TODO: Arturo, if these are commented out, why? Document...
            # BCProtectedNameEntityTypes.BC_COOPERATIVE,
            # BCProtectedNameEntityTypes.BC_COMMUNITY_CONTRIBUTION_COMPANY,
            # XproUnprotectedNameEntityTypes.XPRO_COOPERATIVE
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
