from namex.models import Synonym

from namex.constants import ENTITY_TYPE_END_DESIGNATIONS, ENTITY_TYPE_ANY_DESIGNATIONS, AllEntityTypes
from . import DesignationPositionCodes


class SynonymService:
    _model = None

    def __init__(self):
        # TODO: Not sure if we'll need this later once Model is done
        self._model = Synonym
        print(self._model)

    def get_synonyms(self):
        synonyms = self._model.get_synonym_list()
        return synonyms

    def get_substitutions(self):
        substitutions = self._model.get_substitution_list()
        return substitutions

    def get_stop_words(self):
        stop_words = self._model.get_stop_word_list()
        return stop_words

    def get_designated_start_words(self):
        # start_words = self._model.get_entity_type_designations()
        start_words = []
        return start_words

    def get_designated_end_words(self):
        end_words = self._model.get_entity_type_designations(ENTITY_TYPE_END_DESIGNATIONS, DesignationPositionCodes.END)
        return end_words

    def get_designated_any_words(self):
        any_words = self._model.get_entity_type_designations(ENTITY_TYPE_ANY_DESIGNATIONS, DesignationPositionCodes.ANY)
        return any_words

    def get_designated_end_all_words(self):
        all_entity_types = AllEntityTypes.ALL.value
        end_words = self._model.get_entity_type_designations([AllEntityTypes.ALL], DesignationPositionCodes.END)
        return end_words.get(AllEntityTypes.ALL.value)

    def get_designated_any_all_words(self):
        any_words = self._model.get_entity_type_designations([AllEntityTypes.ALL], DesignationPositionCodes.ANY)
        return any_words.get(AllEntityTypes.ALL.value)
    '''
    stop_words = get_stop_word_list()
    en_designation_any = get_en_designation_any_all_list()
    en_designation_end = get_en_designation_end_all_list()
    fr_designation_end = get_fr_designation_end_list()
    prefixes = get_prefix_list()
    cf = pd.DataFrame(columns=['word', 'word_classification'])
    '''

    '''
    entity_end_designation_dict = {'RLC': get_en_RLC_entity_type_end_designation(),
                                   'LL': get_en_LL_entity_type_end_designation(),
                                   'CC': get_en_CC_entity_type_end_designation(),
                                   'UL': get_en_UL_entity_type_end_designation(),
                                   'BC': get_en_BC_entity_type_end_designation(),
                                   'CR': get_en_CR_entity_type_end_designation()}

    entity_any_designation_dict = {'CP': get_en_CP_entity_type_any_designation(),
                                   'XCP': get_en_XCP_entity_type_any_designation(),
                                   'CC': get_en_CC_entity_type_any_designation()}

    all_designation_any_end_list = get_designations_in_name(name)

    entity_type_end_designation = get_entity_type_end_designation(entity_end_designation_dict,
                                                                  all_designation_any_end_list)
    entity_type_any_designation = get_entity_type_any_designation(entity_any_designation_dict,
                                                                  all_designation_any_end_list)
    entity_type_end_designation = [item for sublist in entity_type_end_designation for item in sublist]
    entity_type_any_designation = [item for sublist in entity_type_any_designation for item in sublist]
    '''
