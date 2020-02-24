import re
from sqlalchemy import func

from namex.models import Synonym
from namex.criteria.synonym.query_criteria import SynonymQueryCriteria

from .mixins.designation import SynonymDesignationMixin
from .mixins.model import SynonymModelMixin

"""
- Services implement business logic, and NON generic queries. 
- Services don't have generic model query methods like find, find_one, or find_by_criteria.
- Methods like find, find_one, or find_by_criteria or iterate belong in models.
"""


class SynonymService(SynonymDesignationMixin, SynonymModelMixin):
    _model = None
    _parse_csv_line = lambda x: (x.split(','))

    def __init__(self):
        # TODO: Not sure if we'll need this later once Model is done
        self._model = Synonym
        print(self._model)

    @classmethod
    def _flatten_synonyms_text(cls, results):
        # Convert tuple results to a list of of CSV strings
        result_arr = [item for sublist in results for item in sublist]
        result_arr = [x.strip() for x in result_arr]

        result_arr = [*map(cls._parse_csv_line, result_arr)]
        flattened_arr = [item for sublist in result_arr for item in sublist]
        return flattened_arr

    def find_word_synonyms(self, word, filters):
        model = self.get_model()
        word = word.lower() if isinstance(word, str) else None

        if word:
            filters.append(func.lower(model.synonyms_text).like(word))

        criteria = SynonymQueryCriteria(
            word=word,
            fields=[self._model.synonyms_text],
            filters=filters
        )

        return model.find_by_criteria(criteria)

    def get_model(self):
        return self._model

    def get_synonyms(self, word='food'):
        model = self.get_model()

        filters = [
            ~func.lower(model.category).op('~')(r'\y{}\y'.format('sub')),
            ~func.lower(model.category).op('~')(r'\y{}\y'.format('stop')),
        ]

        results = self.find_word_synonyms(word, filters)
        flattened = self._flatten_synonyms_text(results)
        return flattened

    def get_substitutions(self, word=None):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('sub'))
        ]

        results = self.find_word_synonyms(word, filters)
        flattened = self._flatten_synonyms_text(results)
        return flattened

    def get_stop_words(self, word=None):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('(stop|stop word[s]?)')),
        ]

        results = self.find_word_synonyms(word, filters)
        flattened = self._flatten_synonyms_text(results)
        return flattened

    def get_prefixes(self):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('prefix(es)?'))
        ]

        results = self.find_word_synonyms(None, filters)
        flattened = self._flatten_synonyms_text(results)
        return flattened

    # TODO: Validate code type args!
    def get_designations(self, entity_type_code, position_code, lang):
        lang = lang if isinstance(lang, str) else 'english'
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}[-_]+valid\y'.format(entity_type_code.value.lower())),
            func.lower(model.category).op('~')(r'\y{}\y'.format('designation[s]?[_-]+' + position_code.value.lower())),
            func.lower(model.category).op('~')(r'\y{}\y'.format(lang.lower()))
        ]

        results = self.find_word_synonyms(None, filters)
        flattened = self._flatten_synonyms_text(results)
        return flattened

    # TODO: Move this out of utils, it uses a model utils shouldn't use class methods
    def regex_transform(self, text, designation_any, designation_end, prefix_list):
        designation_end_regex = '((lot)+\\s+\\d+|\\d*|' + '|'.join(map(str, designation_end)) + ')'
        designation_any_regex = "(" + '|'.join(designation_any) + ")"
        prefixes = '|'.join(prefix_list)

        exceptions_ws = []
        for word in re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE).split():
            if self._model.get_substitution_list(word):
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
        # TODO: Re-enable remove_french!
        # words = remove_french(words, fr_designation_end_list)
        tokens = self.regex_transform(words, designation_any, designation_end, prefix_list)
        tokens = tokens.split()

        return [x.lower() for x in tokens if x]

    def get_all_substitutions_synonyms(self, list_d, distinctive=True):
        aux_list = []
        response_list = []

        for word in list_d:
            if distinctive:
                aux_list = self.get_substitution_list(word)
            else:
                aux_list = self.get_synonym_list(word)
            if aux_list:
                response_list.append(aux_list)
            else:
                response_list.append([word.lower()])

        return response_list

