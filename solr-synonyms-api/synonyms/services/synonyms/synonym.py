import re
from sqlalchemy import func

from synonyms.models.synonym import Synonym
from synonyms.criteria.synonym.query_criteria import SynonymQueryCriteria
from . import LanguageCodes

from .mixins.designation import SynonymDesignationMixin
from .mixins.model import SynonymModelMixin

from synonyms.utils.service_utils import get_entity_type_code, get_designation_position_code

"""
- Services implement business logic, and NON generic queries. 
- Services don't have generic model query methods like find, find_one, or find_by_criteria.
- Methods like find, find_one, or find_by_criteria or iterate belong in models.
"""


class SynonymService(SynonymDesignationMixin, SynonymModelMixin):
    @property
    def _model(self):
        return Synonym

    _parse_csv_line = lambda x: (x.split(','))

    @classmethod
    def flatten_synonyms_text(cls, results):
        # Convert tuple results to a list of of CSV strings
        result_arr = [item for sublist in results for item in sublist]
        result_arr = [x.strip() for x in result_arr]

        result_arr = [*map(cls._parse_csv_line, result_arr)]
        flattened_arr = [item for sublist in result_arr for item in sublist]
        return flattened_arr

    '''
    Designations, distinctives and descriptives return stems_text
    '''

    def find_word_synonyms(self, word, filters):
        model = self.get_model()
        word = word.lower() if isinstance(word, str) else None

        if word:
            filters.append(func.lower(model.synonyms_text).op('~')(r'\y{}\y'.format(word)))

        field = model.stems_text

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

        results = self.find_word_synonyms(None, filters)
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

    def get_designations(self, entity_type_str, position_str, lang):
        lang = lang if isinstance(lang, str) else LanguageCodes.ENG.value
        model = self.get_model()

        entity_type_code = get_entity_type_code(entity_type_str)
        position_code = get_designation_position_code(position_str) if isinstance(position_str, str) else position_str

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

        results = self.find_word_synonyms(None, filters)
        flattened = list(set(map(str.strip, (list(filter(None, self.flatten_synonyms_text(results)))))))
        flattened.sort(key=len, reverse=True)
        return flattened

    '''
    Rules for Regex Transform (from bottom to top):
    1.- Replace with non-space 
        A.- .com: internet_domains
    	B.- Commas in numbers: 50,000 --> 50000 (?<=\\d),(?=\\d)|
    	B.- Set together words followed by punctuation and a character (AB-C, A-C, ABC-C): (?<=\b[A-Za-z])+[\/&-](?=[A-Za-z]\b)
    	C.- Designations anywhere    	
    2.- Search for prefixes followed by punctuation and a word (re/max) and set them together: \b('+prefixes+')([ &\/.-])([A-Za-z]+)
    3.- Replace with space the following:
        A.- Word with possesive such as Reynold's: (?<=[a-zA-Z])\'[Ss]
    	B.- (NO. 111),NO. 465,(LOT 111),LOT 27,LOT( 100-2),(100): \(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d+\)?|\(\d+\)
    	#C.- Punctuation except ampersand, slash, hyphen used for separation: [^a-zA-Z0-9 &/-]+
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
    9.- Replace with non-space:
         Remove numbers and numbers in words at the beginning or keep them as long as the last string is 
         any BC|HOLDINGS|VENTURES: (^(?:\d+(?:{ordinal_suffixes})?\s+)+(?=[^\d]+$)|(?:({numbers})\s+)(?!.*?(?:{stand_alone_words}$))
    	 Set single letters together (initials):(?<=\b[A-Za-z]\b) +(?=[a-zA-Z]\b)
    10.- Remove extra spaces to have just one space: \s+
    '''

    def regex_transform(self, text, designation_all, number_list, exceptions_ws):
        designation_all_regex = '|'.join(designation_all)
        numbers = '|'.join(number_list)
        ordinal_suffixes = 'ST|[RN]D|TH'
        stand_alone_words = 'HOLDINGS$|BC$|VENTURES$|SOLUTION$|ENTERPRISE$|INDUSTRIES$'
        internet_domains = '.COM|.ORG|.NET|.EDU'

        text = self.regex_remove_designations(text, internet_domains, designation_all_regex)
        text = self.regex_numbers_lot(text)
        # text = self.regex_repeated_strings(text)
        text = self.regex_separated_ordinals(text, ordinal_suffixes)
        text = self.regex_keep_together_abv(text, exceptions_ws)
        text = self.regex_punctuation(text)
        text = self.regex_together_one_letter(text)
        text = self.regex_strip_out_numbers_middle_end(text, ordinal_suffixes, numbers)
        text = self.regex_numbers_standalone(text, ordinal_suffixes, numbers, stand_alone_words)
        text = self.regex_remove_extra_spaces(text)

        return text

    @classmethod
    def regex_remove_designations(cls, text, internet_domains, designation_all_regex):
        text = re.sub(r'\b({0})\b|(?<=\d),(?=\d)|(?<=[A-Za-z])+[&-](?=[A-Za-z]\b)|(?<!\w)({1})(?!\w)(?=.*$)'.format(
            internet_domains,
            designation_all_regex),
                      '',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_prefixes(cls, text, prefixes):
        text = re.sub(r'\b({})([ &/.-])([A-Za-z]+)'.format(prefixes),
                      r'\1\3',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_numbers_lot(cls, text):
        text = re.sub(r'(?<=[a-zA-Z])\'[Ss]|\(?No.?\s*\d+\)?|\(?lot.?\s*\d+[-]?\d*\)?|[^a-zA-Z0-9 &/-]+',
                      ' ',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_repeated_strings(cls, text):
        text = re.sub(r'\b(\w{2,})(\b\W+\b\1\b)*',
                      r'\1',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_separated_ordinals(cls, text, ordinal_suffixes):
        text = re.sub(r'\b(\d+({}))(\w+)\b'.format(ordinal_suffixes),
                      r'\1 \3',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_keep_together_abv(cls, text, exceptions_ws):
        exception_ws_rx = '|'.join(map(re.escape, exceptions_ws))
        ws_generic_rx = r'(?<=\d)(?=[^\d\s])|(?<=[^\d\s])(?=\d)'
        ws_rx = re.compile(r'({})|{}'.format(exception_ws_rx, ws_generic_rx), re.I)

        text = ws_rx.sub(lambda x: x.group(1) or " ", text)

        return " ".join(text.split())

    @classmethod
    def regex_punctuation(cls, text):
        text = re.sub(r'[&/-]',
                      ' ',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_together_one_letter(cls, text):
        text = re.sub(r'(\b[A-Za-z]{1,2}\b)\s+(?=[a-zA-Z]{1,2}\b)|\s+$',
                      r'\1',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_strip_out_numbers_middle_end(cls, text, ordinal_suffixes, numbers):
        text = re.sub(r'(?<=[A-Za-z]\b\s)([ 0-9]+({})?\b|({})\b)'.format(ordinal_suffixes, numbers),
                      '',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_numbers_standalone(cls, text, ordinal_suffixes, numbers, stand_alone_words):
        text = re.sub(
            r'\b(?=(\d+(?:{0})?\b(?:\s+\d+(?:\b{0}\b)?)*|(?:\b({1})\b)(?:\s+(?:\b({1})\b))*))\1(?!\s+(?:{2})\b)\s*'.format(
                ordinal_suffixes, numbers, stand_alone_words),
            '',
            text,
            0,
            re.IGNORECASE)
        return " ".join(text.split())

    @classmethod
    def regex_remove_extra_spaces(cls, text):
        text = re.sub(r'\s+',
                      ' ',
                      text,
                      0,
                      re.IGNORECASE)
        return " ".join(text.split())

    def exception_regex(self, text):
        # Build exception list to avoid separation of numbers and letters when they are part of synonym table such as H20, 4MULA, ACTIV8
        exceptions_ws = []
        for word in re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE).split():
            if self.get_substitutions(word):
                exceptions_ws.append(word)

        if not exceptions_ws:
            exceptions_ws.append('null')

        return exceptions_ws
