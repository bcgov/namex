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
        self._model = Synonym

    @classmethod
    def flatten_synonyms_text(cls, results):
        # Convert tuple results to a list of of CSV strings
        result_arr = [item for sublist in results for item in sublist]
        result_arr = [x.strip() for x in result_arr]

        result_arr = [*map(cls._parse_csv_line, result_arr)]
        flattened_arr = [item for sublist in result_arr for item in sublist]
        return flattened_arr

    def find_word_synonyms(self, word, filters, designation=False):
        model = self.get_model()
        # TODO: Don't use an empty string here, instantiate a different SynonymQueryCriteria to handle a case with no fields or set to null or whatever
        field = ''
        word = word.lower() if isinstance(word, str) else None

        if word:
            filters.append(func.lower(model.synonyms_text).op('~')(r'\y{}\y'.format(word)))

        if designation:
            field = model.stems_text
        else:
            field = model.synonyms_text

        criteria = SynonymQueryCriteria(
            word=word,
            fields=[field],
            filters=filters
        )

        return model.find_by_criteria(criteria)

    def get_model(self):
        return self._model

    def get_synonyms(self, word=None):
        model = self.get_model()

        filters = [
            ~func.lower(model.category).op('~')(r'\y{}\y'.format('sub')),
            ~func.lower(model.category).op('~')(r'\y{}\y'.format('stop')),
        ]

        results = self.find_word_synonyms(word, filters)
        flattened = list(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results))))))
        return flattened

    def get_substitutions(self, word=None):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('sub'))
        ]

        results = self.find_word_synonyms(word, filters)
        flattened = list(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results))))))
        return flattened

    def get_stop_words(self, word=None):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('stop word[s]?')),
        ]

        results = self.find_word_synonyms(word, filters)
        flattened = list(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results))))))
        return flattened

    def get_prefixes(self):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('prefix(es)?'))
        ]

        results = self.find_word_synonyms(None, filters, True)
        flattened = list(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results))))))
        return flattened

    def get_number_words(self):
        model = self.get_model()

        filters = [
            func.lower(model.category).op('~')(r'\y{}\y'.format('number(s)? sub')),
        ]

        results = self.find_word_synonyms(None, filters)
        flattened = list(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results))))))
        return flattened

    def get_designations(self, entity_type_code, position_code, lang):
        lang = lang if isinstance(lang, str) else 'english'
        model = self.get_model()

        filters = []

        if entity_type_code is not None:
            filters.append(
                func.lower(model.category).op('~')(r'\y{}[-_]+valid\y'.format(entity_type_code.value.lower())))

        if position_code is not None:
            filters.append(func.lower(model.category).op('~')(
                r'\y{}\y'.format('designation[s]?[_-]+' + position_code.value.lower())))
        else:
            filters.append(func.lower(model.category).op('~')(r'\y{}\y'.format('designation[s]?[_-]')))

        filters.append(func.lower(model.category).op('~')(r'\y{}\y'.format(lang.lower())))

        results = self.find_word_synonyms(None, filters, True)
        flattened = list(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results))))))
        return flattened

    '''
    Rules for Regex Transform (from bottom to top):
    1.- Replace with non-space 
        A.- .com: internet_domains
    	B.- Commas in numbers: 50,000 --> 50000 (?<=\\d),(?=\\d)|
    	B.- Set together words followed by punctuation and a character (AB-C, A-C, ABC-C): (?<=\b[A-Za-z])+[\/&-](?=[A-Za-z]\b)
    	C.- Designations anywhere
    	E.- Designations and numbers at the end: re.sub(r'\s('+desig_end+')$'
    2.- Search for prefixes followed by punctuation and a word (re/max) and set them together: \b('+prefixes+')([ &\/.-])([A-Za-z]+)
    3.- Replace with space the following:
        A.- Word with possesive such as Reynold's: (?<=[a-zA-Z])\'[Ss]
    	B.- (NO. 111),NO. 465,(LOT 111),LOT 27,LOT( 100-2),(100): \(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d+\)?|\(\d+\)
    	C.- Punctuation except ampersand, slash, hyphen used for separation: [^a-zA-Z0-9 &/-]+
    4.- Remove repeated strings with minimum two characters (AB -- AB --> AB): \b(\w{2,})(\b\W+\b\1\b)*
    5.- Separate ordinal numbers from words (4THGEN --> 4TH GEN):\b(\d+(ST|[RN]D|TH))(\w+)\b
    6.- Replace with space: 
        Alphanumeric strings separating strings from letters as long as they are not in exception list (substitution list):
        For instance 1st,h20 are not separated because they are in substitution list, but P8 is transformed to P 8 
          rx=re.compile(rf'({exception_rx})|{generic_rx}', re.I)
    	  rx.sub(lambda x: x.group(1) or " "
    7.- Replace with space:
        Punctuation including ampersand, slash, hyphen used for separation:[&/-]
    8.- Replace with non-space:
         Set together letter of length one separated by spaces: (?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)
    	 Trailing and leading spaces in string: ^\s+|\s+$
    9.- Replace with non-space the following:
        A.- Remove cardinal and ordinal numbers from string in the middle and end: (?<=[A-Za-z]\b )([ 0-9]*(ST|[RN]D|TH)?\b)
        #(Note: May be removed) B.- Set together numbers separated by more than 2 spaces: (?<=\d)\s{2,}(?=\d+).
    10.- Replace with non-space:
         Remove numbers and numbers in words at the beginning or keep them as long as the last string is 
         any BC|HOLDINGS|VENTURES: (^(?:\d+(?:{ordinal_suffixes})?\s+)+(?=[^\d]+$)|(?:({numbers})\s+)(?!.*?(?:{stand_alone_words}$))
    	 Set single letters together (initials):(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)
    11.- Remove extra spaces to have just one space: \s+
    '''

    def regex_transform(self, text, designation_any, designation_end, designation_all, prefix_list, number_list):
        designation_end_regex = '((lot)+\\s+\\d+|\\d*|' + '|'.join(map(str, designation_end)) + ')'
        designation_any_regex = "(" + '|'.join(designation_any) + ")"
        designation_all_regex = "(" + '|'.join(designation_all) + ")"
        prefixes = '|'.join(prefix_list)
        numbers = '|'.join(number_list)
        ordinal_suffixes = 'ST|[RN]D|TH'
        stand_alone_words = 'HOLDINGS$|BC$|VENTURES$|SOLUTION$|ENTERPRISE$|INDUSTRIES$'
        internet_domains = '.COM'

        # Build exception list to avoid separation of numbers and letters when they are part of synonym table such as H20, 4MULA, ACTIV8
        exceptions_ws = []
        for word in re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE).split():
            if self.get_substitutions(word):
                exceptions_ws.append(word)

        if not exceptions_ws:
            exceptions_ws.append('null')

        exception_ws_rx = '|'.join(map(re.escape, exceptions_ws))
        ws_generic_rx = r'(?<=\d)(?=[^\d\s])|(?<=[^\d\s])(?=\d)'
        ws_rx = re.compile(rf'({exception_ws_rx})|{ws_generic_rx}', re.I)

        text = re.sub(r'\s+',
                      ' ',
                      re.sub(
                          r'(^(?:\d+(?:' + ordinal_suffixes + ')?\\s+)+(?=[^\\d]+$)|(?:' + numbers + ')\\s+)(?!.*?(?:' + stand_alone_words + '$))|(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)',
                          '',
                          re.sub(r'(?<=[A-Za-z]\b )([ 0-9]*(' + ordinal_suffixes + ')?\b)',
                                 '',
                                 re.sub(r'(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)|^\s+|\s+$',
                                        '',
                                        re.sub(r'[&/-]',
                                               ' ',
                                               # re.sub(r'(?<=[0-9])\s+(?=(?:{ordinal_suffixes})(?: +[^\W\d_]|$))',
                                               #       '',
                                               ws_rx.sub(lambda x: x.group(1) or " ",
                                                         re.sub(r'\b(\d+(' + ordinal_suffixes + '))(\\w+)\\b',
                                                                r'\1 \3',
                                                                re.sub(r'\b(\w{2,})(\b\W+\b\1\b)*',
                                                                       r'\1',
                                                                       re.sub(
                                                                           r'(?<=[a-zA-Z])\'[Ss]|\(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d*\)?|[^a-zA-Z0-9 &/-]+',
                                                                           ' ',
                                                                           re.sub(
                                                                               r'\b(' + prefixes + ')([ &/.-])([A-Za-z]+)',
                                                                               r'\1\3',
                                                                               re.sub(
                                                                                   # rf"\.COM|(?<=\d),(?=\d)|(?<=[A-Za-z])+[\/&-](?=[A-Za-z]\b)|\b{designation_any_regex}\b|\s{designation_end_regex}(?=(\s{designation_end_regex})*$)",
                                                                                   rf"\.COM|(?<=\d),(?=\d)|(?<=[A-Za-z])+[\/&-](?=[A-Za-z]\b)|\b{designation_all_regex}\b",
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
                                                                0,
                                                                re.IGNORECASE),
                                                         ),
                                               # 0,
                                               # re.IGNORECASE),
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
