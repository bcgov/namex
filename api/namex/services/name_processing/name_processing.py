import re
import warnings

from ..name_request.auto_analyse.name_analysis_utils import remove_french, remove_stop_words

from namex.services.synonyms.synonym import SynonymService
from namex.services.word_classification.word_classification import WordClassificationService

from .mixins.get_synonym_lists import GetSynonymListsMixin

'''
Service for pre-processing of a user submitted name request name string.
Setting the name using NameProcessingService.set_name will clean the name and set the following properties:
@:prop name_as_submitted The original name string
@:prop name_as_submitted_tokenized The original name tokenized handling designations as one token. 
                                    For instance, if original name has limited liability company, this compound designation is made a token.
@:prop name_original_tokens The original name tokenized without any special handling.
@:prop processed_name The cleaned name
@:prop name_tokens Word tokens generated from the cleaned name
'''


class NameProcessingService(GetSynonymListsMixin):
    @property
    def name_as_submitted(self):
        return self._name_as_submitted

    @property
    def name_as_submitted_tokenized(self):
        return self._name_as_submitted_tokenized

    @property
    def name_original_tokens(self):
        return self._name_original_tokens

    @name_as_submitted.setter
    def name_as_submitted(self, val):
        self._name_as_submitted = val

    @name_as_submitted_tokenized.setter
    def name_as_submitted_tokenized(self, val):
        self._name_as_submitted_tokenized = val

    @name_original_tokens.setter
    def name_original_tokens(self, val):
        self._name_original_tokens = val

    @property
    def processed_name(self):
        return self._processed_name

    @processed_name.setter
    def processed_name(self, val):
        self._processed_name = val

    @property
    def name_tokens(self):
        return self._name_tokens

    @name_tokens.setter
    def name_tokens(self, val):
        self._name_tokens = val

    @property
    def word_classification_service(self):
        return self._word_classification_service

    @word_classification_service.setter
    def word_classification_service(self, svc):
        self._word_classification_service = svc

    @property
    def synonym_service(self):
        return self._synonym_service

    @synonym_service.setter
    def synonym_service(self, svc):
        self._synonym_service = svc

    def __init__(self):
        self.synonym_service = SynonymService()
        self.word_classification_service = WordClassificationService()
        self.name_as_submitted = None
        self.name_as_submitted_tokenized = None
        self.name_original_tokens = None
        self.processed_name = None
        self.name_tokens = None
        self.distinctive_word_tokens = None
        self.descriptive_word_tokens = None
        self.unclassified_word_tokens = None

    '''
    Set and process a submitted name string using the process_name class method.
    '''
    def set_name(self, name):
        self.name_as_submitted = name  # Store the user's submitted name string
        self.name_original_tokens = name.lower().split()
        self._process_name()

    def set_name_tokenized(self, name):
        all_designations = self._designated_all_words
        all_designations.sort(key=len, reverse=True)
        designation_alternators = '|'.join(map(re.escape, all_designations))
        regex = re.compile(r'(?<!\w)({}|[a-z-A-Z]+)(?!\w)'.format(designation_alternators))
        self.name_as_submitted_tokenized = regex.findall(name.lower())

    def _clean_name_words(self, text, stop_words=[], designation_any=[], designation_end=[], designation_all=[], fr_designation_end_list=[], prefix_list=[], number_list=[]):
        if not text or not stop_words or not designation_any or not designation_end or not prefix_list and not number_list:
            warnings.warn("Parameters in clean_name_words function are not set.", Warning)

        syn_svc = self.synonym_service

        words = remove_stop_words(self.name_original_tokens, stop_words)
        words = remove_french(words)
        exceptions_ws = syn_svc.exception_regex(words)
        tokens = syn_svc.regex_transform(words, designation_all, prefix_list, number_list, exceptions_ws)
        tokens = tokens.split()

        return [x.lower() for x in tokens if x]

    def _prepare_data(self):
        syn_svc = self.synonym_service

        # Query database for word designations
        # These properties are mixed in via GetSynonymListsMixin
        # See the class constructor
        self._stop_words = syn_svc.get_stop_words()
        self._prefixes = syn_svc.get_prefixes()
        self._number_words = syn_svc.get_number_words()
        self._designated_end_words = syn_svc.get_designated_end_all_words()
        self._designated_any_words = syn_svc.get_designated_any_all_words()
        self._designated_all_words = list(set(self._designated_any_words +
                                              self._designated_end_words))
        self._designated_all_words.sort(key=len, reverse=True)
        # TODO: Handle french designations
        self._fr_designation_end_list = []

    '''
    Split a name string into classifiable tokens. Called whenever set_name is invoked.
    @:param string:name
    '''
    def _process_name(self):
        try:
            # Prepare any data that we need to pre-process the name
            self._prepare_data()

            # Clean the provided name and tokenize the string
            self.name_tokens = self._clean_name_words(
                self.name_as_submitted,
                # These properties are mixed in via GetSynonymListsMixin
                # See the class constructor
                self._stop_words,
                self._designated_any_words,
                self._designated_end_words,
                self._designated_all_words,
                self._fr_designation_end_list,
                self._prefixes,
                self._number_words
            )

            # Store clean, processed name to instance
            clean_name = ' '.join(map(str, self.name_tokens))
            self.processed_name = clean_name
            print('Processed name: ' + self.processed_name)

        except Exception as error:
            print('Pre-processing name failed: ' + repr(error))
            raise
