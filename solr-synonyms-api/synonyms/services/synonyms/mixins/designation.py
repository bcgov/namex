import re
import collections

from synonyms.constants import \
    BCProtectedNameEntityTypes, BCUnprotectedNameEntityTypes, XproUnprotectedNameEntityTypes

from . import SynonymServiceMixin
from .. import DesignationPositionCodes, LanguageCodes


class SynonymDesignationMixin(SynonymServiceMixin):
    def get_designated_end_all_words(self, lang):
        lang = lang if isinstance(lang, str) else LanguageCodes.ENG.value
        return self.get_designations(None, DesignationPositionCodes.END.value, lang)

    def get_designated_any_all_words(self, lang):
        lang = lang if isinstance(lang, str) else LanguageCodes.ENG.value
        return self.get_designations(None, DesignationPositionCodes.ANY, lang)

    # TODO: Fix / check this Arturo!
    def get_misplaced_end_designations(self, name, designation_end_entity_type):
        if not designation_end_entity_type:
            return list()
        designation_end_rgx = '(' + '|'.join(map(str, designation_end_entity_type)) + ')'
        designation_end_regex = r'\b{}\s'.format(designation_end_rgx)

        # Returns list of tuples
        misplaced_designation_end_list = re.findall(designation_end_regex, name.lower())

        return misplaced_designation_end_list

    # TODO: Fix / check this Arturo!
    def get_misplaced_any_designations(self, name, designation_any_entity_type):
        if not designation_any_entity_type:
            return list()
        designation_any_rgx = '(' + '|'.join(map(str, designation_any_entity_type)) + ')'
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
        eng_designation_end_all_list = self.get_designations(None, DesignationPositionCodes.END,
                                                             LanguageCodes.ENG.value)
        fr_designation_end_all_list = self.get_designations(None, DesignationPositionCodes.END,
                                                            LanguageCodes.FR.value)

        designation_end_all_list = eng_designation_end_all_list + fr_designation_end_all_list
        designation_end_all_list.sort(key=len, reverse=True)
        designation_end_rgx = '(' + '|'.join(map(str, designation_end_all_list)) + ')'
        designation_end_regex = r'{0}(?=(\s{0})*$)'.format(designation_end_rgx)

        # Returns list of tuples
        designation_end_list = re.findall(designation_end_regex, name.lower())

        designation_end_list = [designation[0].strip() for designation in designation_end_list if designation[0]]

        return designation_end_list

    '''
        Get designations with <end> position for any entity type which have incorrect position different to <end>.
        Designations in <end> position which are at the beginning, middle or before <end> position, these designations
        have to be shown as misplaced.
    '''

    def get_incorrect_designation_end_in_name(self, tokenized_name, designation_end_entity_type):
        if not designation_end_entity_type:
            return list()

        found_incorrect_designation_end = list()
        for token in tokenized_name[:-1]:
            if token in designation_end_entity_type:
                found_incorrect_designation_end.extend([token])

        return found_incorrect_designation_end

    '''
    Get designations with <any> position for any entity type. This omits the general designation with <any> position:
    English Designations_any Stop
    '''

    def get_designation_any_in_name(self, name):
        eng_designation_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY,
                                                             LanguageCodes.ENG.value)
        fr_designation_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY,
                                                            LanguageCodes.FR.value)

        designation_any_all_list = eng_designation_any_all_list + fr_designation_any_all_list
        designation_any_all_list.sort(key=len, reverse=True)

        designation_any_rgx = '(' + '|'.join(map(str, designation_any_all_list)) + ')'
        designation_any_regex = r'(?<!\w)({0})(?!\w)(?=\s|$)'.format(designation_any_rgx)

        # Returns list of tuples
        found_designation_any = re.findall(designation_any_regex, name.lower())
        found_designation_any = list(set([x for designation in found_designation_any for x in designation]))

        return found_designation_any

    '''
        Get all designations in name, these can be misplaced or not.
        '''

    def get_designation_all_in_name(self, name):
        eng_all_designations_end_all_list = self.get_designations(None, DesignationPositionCodes.END,
                                                                  LanguageCodes.ENG.value)
        eng_all_designations_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY,
                                                                  LanguageCodes.ENG.value)

        fr_all_designations_end_all_list = self.get_designations(None, DesignationPositionCodes.END,
                                                                 LanguageCodes.FR.value)
        fr_all_designations_any_all_list = self.get_designations(None, DesignationPositionCodes.ANY,
                                                                 LanguageCodes.FR.value)

        all_designations_end_all_list = eng_all_designations_end_all_list + fr_all_designations_end_all_list
        all_designations_any_all_list = eng_all_designations_any_all_list + fr_all_designations_any_all_list

        all_designations = list(set(all_designations_end_all_list + all_designations_any_all_list))
        all_designations.sort(key=len, reverse=True)

        all_designations_rgx = '|'.join(map(str, all_designations))
        all_designations_regex = r'(?<!\w)({0})(?!\w)(?=\s|$)'.format(all_designations_rgx)

        # Returns list of tuples
        found_all_designations = re.findall(all_designations_regex, name.lower())

        return found_all_designations

    def get_all_end_designations(self):
        entity_types = [
            XproUnprotectedNameEntityTypes.XPRO_LIMITED_LIABILITY_COMPANY,
            BCUnprotectedNameEntityTypes.LIMITED_LIABILITY_PARTNERSHIP,
            BCProtectedNameEntityTypes.UNLIMITED_LIABILITY_COMPANY,
            BCProtectedNameEntityTypes.CORPORATION
        ]

        entity_end_designation_dict = {}

        for entity_type in entity_types:
            entity_end_designation_dict[entity_type.value] = self.get_designations(
                entity_type,
                DesignationPositionCodes.END,
                LanguageCodes.ENG
            )
            eng_designation_end = self.get_designations(entity_type.value, DesignationPositionCodes.END,
                                                        LanguageCodes.ENG.value)
            fr_designation_end = self.get_designations(entity_type.value, DesignationPositionCodes.END,
                                                       LanguageCodes.FR.value)

            designation_end = eng_designation_end + fr_designation_end
            designation_end.sort(key=len, reverse=True)

            entity_end_designation_dict[entity_type.value] = designation_end

        output = []
        for key in entity_end_designation_dict:
            output.append({
                'key': key,
                'list': entity_end_designation_dict[key]
            })

        return output

    def get_all_any_designations(self):
        entity_types = [
        ]

        entity_any_designation_dict = {}

        for entity_type in entity_types:
            eng_designation_any = self.get_designations(entity_type, DesignationPositionCodes.ANY,
                                                        LanguageCodes.ENG.value)
            fr_designation_any = self.get_designations(entity_type, DesignationPositionCodes.ANY,
                                                       LanguageCodes.FR.value)
            designation_any = eng_designation_any + fr_designation_any
            designation_any.sort(key=len, reverse=True)

            entity_any_designation_dict[entity_type.value] = designation_any

        output = []
        for key in entity_any_designation_dict:
            output.append({
                'key': key,
                'list': entity_any_designation_dict[key]
            })

        return output

    def get_entity_type_by_value(self, entity_type_dicts, designation):
        entity_list = list()
        entity__designation_end_list = entity_type_dicts.items()
        print(entity__designation_end_list)
        for entity_designation in entity__designation_end_list:
            if any(designation in value for value in entity_designation[1]):
                entity_list.append(entity_designation[0])
        return entity_list
