import re
import warnings

from flask.globals import current_app
from swagger_client import SynonymsApi as SynonymService

from namex.services.word_classification.word_classification import WordClassificationService

from ..name_request.auto_analyse.mixins.get_designations_lists import GetDesignationsListsMixin
from ..name_request.auto_analyse.name_analysis_utils import remove_french, remove_stop_words
from ..virtual_word_condition.virtual_word_condition import VirtualWordConditionService
from . import LanguageCodes
from .mixins.get_synonym_lists import GetSynonymListsMixin

"""
Service for pre-processing of a user submitted name request name string.
Setting the name using NameProcessingService.set_name will clean the name and set the following properties:
@:prop name_as_submitted The original name string
@:prop name_as_submitted_tokenized The original name tokenized handling designations as one token. 
                                    For instance, if original name has limited liability company, this compound designation is made a token.
@:prop name_original_tokens The original name tokenized without any special handling.
@:prop processed_name The cleaned name
@:prop name_tokens Word tokens generated from the cleaned name
"""


class NameProcessingService(GetSynonymListsMixin, GetDesignationsListsMixin):
    @property
    def name_as_submitted(self):
        return self._name_as_submitted

    @property
    def name_first_part(self):
        return self._name_first_part

    @property
    def name_as_submitted_tokenized(self):
        return self._name_as_submitted_tokenized

    @property
    def name_original_tokens(self):
        return self._name_original_tokens

    @name_as_submitted.setter
    def name_as_submitted(self, val):
        self._name_as_submitted = val

    @name_first_part.setter
    def name_first_part(self, val):
        self._name_first_part = val

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
    def compound_descriptive_name_tokens(self):
        return self._compound_descriptive_name_tokens

    @compound_descriptive_name_tokens.setter
    def compound_descriptive_name_tokens(self, val):
        self._compound_descriptive_name_tokens = val

    @property
    def name_tokens_search_conflict(self):
        return self._name_tokens_search_conflict

    @name_tokens_search_conflict.setter
    def name_tokens_search_conflict(self, val):
        self._name_tokens_search_conflict = val

    @property
    def stop_words(self):
        return self._stop_words

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

    @property
    def virtual_word_condition_service(self):
        return self._virtual_word_condition_service

    @virtual_word_condition_service.setter
    def virtual_word_condition_service(self, svc):
        self._virtual_word_condition_service = svc

    def __init__(self):
        self.synonym_service = SynonymService()
        self.word_classification_service = WordClassificationService()
        self.virtual_word_condition_service = VirtualWordConditionService()
        self.name_as_submitted = None
        self._name_first_part = None
        self.name_as_submitted_tokenized = None
        self.name_original_tokens = None
        self.processed_name = None
        self.name_tokens = None
        self._compound_descriptive_name_tokens = None
        self.name_tokens_search_conflict = None
        self.distinctive_word_tokens = None
        self.descriptive_word_tokens = None
        self.unclassified_word_tokens = None

    """
    Set and process a submitted name string using the process_name class method.
    """

    def set_name(self, name, np_svc_prep_data):
        self.name_as_submitted = name  # Store the user's submitted name string
        self._process_name(np_svc_prep_data)

    def set_name_tokenized(self, name):
        all_designations = self._designated_all_words
        all_designations.sort(key=len, reverse=True)
        designation_alternators = '|'.join(map(re.escape, all_designations))
        regex = re.compile(r'(?<!\w)({}|[a-z-A-Z0-9]+)(?!\w)'.format(designation_alternators))
        self.name_as_submitted_tokenized = regex.findall(name.lower())

    def _clean_name_words(self, name, stop_words=[], designation_all=[], prefix_list=[], number_list=[]):
        if not name or not stop_words or not designation_all or not prefix_list or not number_list:
            warnings.warn('Parameters in clean_name_words function are not set.', Warning)

        syn_svc = self.synonym_service
        # vwc_svc = self.virtual_word_condition_service
        designation_all.sort(key=len, reverse=True)
        designation_alternators = '|'.join(map(re.escape, designation_all))

        exception_designation = self.exception_designation(name)
        exception_stop_words_designation = list(set(self.exception_designation_stop_word(stop_words, designation_all)))
        exception_stop_words_designation.sort(key=len, reverse=True)

        name_original_tokens = [x for x in [x.strip() for x in re.split('([ &/-])', name.lower())] if x]
        self.name_original_tokens = name_original_tokens

        name = remove_stop_words(name, stop_words, exception_stop_words_designation)

        prefixes = '|'.join(prefix_list)
        words = syn_svc.get_regex_prefixes(
            text=name, prefixes_str=prefixes, exception_designation=exception_designation
        ).data

        name = remove_french(words, designation_alternators)
        self.name_first_part = name

        # exceptions_ws = syn_svc.get_exception_regex(text=name).data
        # exceptions_ws.extend(self.exception_virtual_word_condition(name, vwc_svc))

        tokens = syn_svc.get_transform_text(
            text=name,
            designation_all=designation_all,
            prefix_list=prefix_list,
            number_list=number_list,
            exceptions_ws=[],
        ).data

        tokens = tokens.split()

        return [x.lower() for x in tokens if x]

    def exception_virtual_word_condition(self, text, vwc_svc):
        exceptions_ws = []
        for word in re.sub(r'[^a-zA-Z0-9 -\']+', ' ', text, 0, re.IGNORECASE).split():
            if vwc_svc.get_word(word) and bool(re.search(r'\d', word)):
                exceptions_ws.append(word)

        if not exceptions_ws:
            exceptions_ws.append('null')

        return exceptions_ws

    def exception_designation(self, text):
        exceptions_designation = []
        all_designations = self._designated_all_words
        designations_with_hyphen = [designation for designation in all_designations if '-' in designation]

        exceptions_designation = [designation for designation in designations_with_hyphen if designation in text]

        if not exceptions_designation:
            exceptions_designation.append('null')

        return exceptions_designation

    def exception_designation_stop_word(self, stop_words, all_designations):
        exception_stopword_designation = []
        for word in stop_words:
            for designation in all_designations:
                if bool(re.search(r'\b{0}\b'.format(word), designation)):
                    exception_stopword_designation.append(designation)

        if not exception_stopword_designation:
            exception_stopword_designation.append('null')

        return exception_stopword_designation

    def prepare_data(self):
        """Prep the analysis."""
        syn_svc = self.synonym_service

        # Query database for word designations
        # These properties are mixed in via GetSynonymListsMixin
        # See the class constructor
        self._stop_words = syn_svc.get_stop_words().data
        self._prefixes = syn_svc.get_prefixes().data
        self._number_words = syn_svc.get_number_words().data
        self._stand_alone_words = syn_svc.get_stand_alone().data

        self._eng_designated_end_words = syn_svc.get_designated_end_all_words(lang=LanguageCodes.ENG.value).data
        self._eng_designated_any_words = syn_svc.get_designated_any_all_words(lang=LanguageCodes.ENG.value).data

        self._fr_designated_end_words = syn_svc.get_designated_end_all_words(lang=LanguageCodes.FR.value).data
        self._fr_designated_any_words = syn_svc.get_designated_any_all_words(lang=LanguageCodes.FR.value).data

        self._designated_end_words = self._eng_designated_end_words + self._fr_designated_end_words
        self._designated_any_words = self._eng_designated_any_words + self._fr_designated_any_words

        self._designated_all_words = list(set(self._designated_any_words + self._designated_end_words))
        self._designated_all_words.sort(key=len, reverse=True)

    def _process_name(self, np_svc_prep_data):
        """Split a name string into classifiable tokens.

        Called whenever set_name is invoked.
        """
        try:
            # Clean the provided name and tokenize the string
            self.name_tokens = self._clean_name_words(
                self.name_as_submitted,
                # These properties are mixed in via GetSynonymListsMixin
                # See the class constructor
                np_svc_prep_data.get_stop_words(),
                np_svc_prep_data.get_designated_all_words(),
                np_svc_prep_data.get_prefixes(),
                np_svc_prep_data.get_number_words(),
            )

            # Store clean, processed name to instance
            clean_name = ' '.join(map(str, self.name_tokens))
            self.processed_name = clean_name
            current_app.logger.debug('Processed name: ' + self.processed_name)

        except Exception as error:
            current_app.logger.error('Pre-processing name failed: ' + repr(error))
            raise
