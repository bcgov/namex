import re
import collections
from namex.models import Synonym

from namex.constants import ENTITY_TYPE_END_DESIGNATIONS, ENTITY_TYPE_ANY_DESIGNATIONS, AllEntityTypes
from . import DesignationPositionCodes


class SynonymService:
    _model = None

    def __init__(self):
        # TODO: Not sure if we'll need this later once Model is done
        self._model = Synonym
        print(self._model)

    def get_model(self):
        return self._model

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

    def get_wrong_place_end_designations(self, name):
        en_designation_end_all_list = self.get_model().get_en_designation_end_all_list()
        designation_any_rgx = '(' + '|'.join(map(str, en_designation_end_all_list)) + ')'
        designation_any_regex = r'\b' + designation_any_rgx + '(?=\s)'

        # Returns list of tuples
        wrong_designation_any_list = re.findall(designation_any_regex, name.lower())

        return wrong_designation_any_list

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
                self.get_model().get_entity_type_by_value(entity_any_designation_dict, designation_any))

        all_entity_types = [item for item, count in collections.Counter(entity_type_any_designation_name).items() if
                            count > 1]

        if all_entity_types:
            return all_entity_types

        return entity_type_any_designation_name

    def get_designation_end_in_name(self, name):
        en_designation_end_all_list = self.get_model().get_en_designation_end_all_list()
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

    def get_designation_any_in_name(self, name):
        en_designation_any_all_list = self.get_model().get_en_designation_any_all_list()
        designation_any_rgx = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
        designation_any_regex = r'\b' + designation_any_rgx + '(?=\s)'

        # Returns list of tuples
        found_designation_any = re.findall(designation_any_regex, name.lower())

        return found_designation_any

    def get_wrong_place_any_designations(self, name):
        en_designation_any_all_list = self.get_model().get_en_designation_any_all_list()

        designation_end_rgx = '(' + '|'.join(map(str, en_designation_any_all_list)) + ')'
        designation_end_regex = r'' + designation_end_rgx + '(?=(\s' + designation_end_rgx + ')*$)'

        # Returns list of tuples
        found_designation_end = re.findall(designation_end_regex, name.lower())

        # Getting list of lists where the first list contains designations of type "anywhere" and the second list contains designations of type "end".
        # [['association],['limited partnership']
        wrong_designation_end_list = [list(elem) for elem in found_designation_end]
        if any(isinstance(el, list) for el in wrong_designation_end_list):
            wrong_designation_end_list = get_flat_list(wrong_designation_end_list)
        wrong_designation_end_list = list(filter(None, wrong_designation_end_list))
        wrong_designation_end_list = list(dict.fromkeys(wrong_designation_end_list))

        return wrong_designation_end_list

    # TODO: Move this out of utils, it uses a model utils shouldn't use class methods
    def regex_transform(self, text, designation_any, designation_end, prefix_list):
        designation_end_regex = '((lot)+\\s+\\d+|\\d*|' + '|'.join(map(str, designation_end)) + ')'
        designation_any_regex = "(" + '|'.join(designation_any.value.tolist()) + ")"
        prefixes = '|'.join(prefix_list)

        exceptions_ws = []
        for word in re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE).split():
            if self.get_substitution_list(word):
                exceptions_ws.append(word)

        if not exceptions_ws:
            exceptions_ws.append('null')

        exception_ws_rx = '|'.join(map(re.escape, exceptions_ws))
        ws_generic_rx = r'(?<=\d)(?=[^\d\s])|(?<=[^\d\s])(?=\d)'
        ws_rx = re.compile(rf'({exception_ws_rx})|{ws_generic_rx}', re.I)

        text = re.sub(r'\s+',
                      ' ',
                      re.sub(
                          r'^(?:\d+(?:ST|[RN]D|TH)?\s+)+(?=[^\d]+$)(?!.*?(?:HOLDINGS$|BC$|VENTURES$))|(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)',
                          '',
                          re.sub(r'(?<=[A-Za-z]\b )([ 0-9]*(ST|[RN]D|TH)?\b)',
                                 '',
                                 re.sub(r'(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)|^\s+|\s+$',
                                        '',
                                        re.sub(r'[&/-]',
                                               ' ',
                                               ws_rx.sub(lambda x: x.group(1) or " ",
                                                         re.sub(r'\b(\d+(ST|[RN]D|TH))(\w+)\b',
                                                                r'\1 \3',
                                                                re.sub(r'\b(\w{2,})(\b\W+\b\1\b)*',
                                                                       r'\1',
                                                                       re.sub(
                                                                           r'(?<=[a-zA-Z])\'[Ss]|\(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d*\)?|[^a-zA-Z0-9 &/-]+',
                                                                           ' ',
                                                                           re.sub(
                                                                               r'\.COM|(?<=\d),(?=\d)|(?<=[A-Za-z])+[\/&-](?=[A-Za-z]\b)|\b' + designation_any_regex + '\\b|\\s' + designation_end_regex + '(?=(\\s' + designation_end_regex + ')*$)',
                                                                               '',
                                                                               text,
                                                                               0,
                                                                               re.IGNORECASE),
                                                                           0,
                                                                           re.IGNORECASE),
                                                                       0,
                                                                       re.IGNORECASE),
                                                                0,
                                                                re.IGNORECASE),
                                                         ),
                                               0,
                                               re.IGNORECASE),
                                        0,
                                        re.IGNORECASE),
                                 0,
                                 re.IGNORECASE),
                          0,
                          re.IGNORECASE),
                      0,
                      re.IGNORECASE)
        return text

    # TODO: This was moved to name processing
    def clean_name_words(self, text, stop_words=[], designation_any=[], designation_end=[], fr_designation_end_list=[],
                         prefix_list=[]):
        # TODO: Warn or something if params aren't set!
        words = text.lower()
        words = ' '.join([word for x, word in enumerate(words.split(" ")) if x == 0 or word not in stop_words])
        words = remove_french(words, fr_designation_end_list)
        tokens = self.regex_transform(words, designation_any, designation_end, prefix_list)
        tokens = tokens.split()

        return [x.lower() for x in tokens if x]
