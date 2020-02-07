from .name_analysis_utils import clean_name_words


class ProcedureResult:
    def __init__(self, **kwargs):
        self.is_valid = kwargs.get('is_valid', False)
        self.result_code = kwargs.get('result_code', None)

from . import ProcedureResult

from .mixins.get_synonyms_lists import GetSynonymsListsMixin
from .mixins.get_designations_lists import GetDesignationsListsMixin
from .mixins.get_word_classification_lists import GetWordClassificationListsMixin


class AbstractNameAnalysisBuilder(GetSynonymsListsMixin, GetDesignationsListsMixin, GetWordClassificationListsMixin):
    __metaclass__ = abc.ABCMeta

    _name = ''
    _list_name_words = []
    _list_dist_words = []
    _list_desc_words = []
    _list_none_words = []

    @director.setter
    def director(self, director):
        self._director = director

    @property
    def name_processing_service(self):
        return self._name_processing_service

    def set_list_name(self, list_words):
        self._list_name_words = list_words

    def get_list_name(self):
        return self._list_name_words

    def set_list_dist(self, list_words):
        self._list_dist_words = list_words

    def get_list_dist(self):
        return self._list_dist_words

    def set_list_desc(self, list_words):
        self._list_desc_words = list_words

    def get_list_desc(self):
        return self._list_desc_words

    def get_list_none(self):
        return self._list_none_words

    def set_list_none(self, list_words):
        self._list_none_words = list_words

    def set_dicts(self, **kwargs):
        self._synonyms = kwargs.get('synonyms')
        self._substitutions = kwargs.get('substitutions')

    @property
    def word_classification_service(self):
        return self._word_classification_service

    @word_classification_service.setter
    def word_classification_service(self, svc):
        self._word_classification_service = svc

    @property
    def word_condition_service(self):
        return self._word_condition_service

    def preprocess_name(self):
        if not self.get_name():
            return  # TODO: Should we throw an error or something?

        words = self.get_name().lower()

        words = ' '.join([word for word in words.split(" ") if word not in self._stop_words])
        # TODO: clean_name_words mostly applies regex substitutions...
        #  but are we moving the regex out of the app and into the database?
        tokens = clean_name_words(words)

        previous = tokens
        for i in range(len(tokens)):
            tokens = clean_name_words(tokens, self._designated_any_words, self._designated_end_words)
            if previous == tokens:
                break
            else:
                previous = tokens

        tokens = tokens.split()
        return [x.upper() for x in tokens if x]

    '''
    This method is NOT abstract and should NEVER be overridden
    @return ProcedureResult
    '''
    def execute_analysis(self):
        return self.do_analysis()

    '''
    This method can be overridden in extending Builder classes if a different process is desired
    @return ProcedureResult
    '''
    def do_analysis(self):
        check_name_is_well_formed = self.check_name_is_well_formed(self.get_list_dist(), self.get_list_desc(), self.get_list_name())
        check_words_to_avoid = self.check_words_to_avoid()
        check_conflicts = self.search_conflicts(self.get_list_dist(), self.get_list_desc())
        check_words_requiring_consent = self.check_words_requiring_consent()
        check_designation_mismatch = self.check_designation()

    @synonym_service.setter
    def synonym_service(self, svc):
        self._synonym_service = svc

    @property
    def entity_type(self):
        return self.director.entity_type

    def __init__(self, director):
        # Store a reference to the director, we will need to access methods on the director instance to do things
        # like updating the classifications table
        self.director = director

        self.name_processing_service = director.name_processing_service
        self.word_classification_service = director.word_classification_service
        self.word_condition_service = director.word_condition_service
        self.synonym_service = director.synonym_service

    # Just a wrapped call to the API's getClassification
    def get_word_classification(self, word):
        return self.word_classification_service.find_one(word)

    # Just a wrapped call to the API's updateClassification
    def update_word_classification(self, word_classification):
        return self.word_classification_service.update(word_classification)

    '''
    Check to see if a provided name is valid
    @return ProcedureResult
    '''
    def check_name_is_well_formed(self, list_dist, list_desc, company_name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    
    The reason this check is done separately from check_name_is_well_formed is
    because out of province / intl names may not follow the same analysis rules.
    Having this check separate allows us the flexibility of checking for words
    to avoid specifically in cases where it is necessary.
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def check_words_to_avoid(self, list_name, name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def search_conflicts(self, list_dist, list_desc, list_name, name):
        return ProcedureResult(is_valid=True)

    # Default handler - this method should be overridden in extending Builder classes
    # def _search_conflicts_success(self):
    #    pass

    # Default handler - this method should be overridden in extending Builder classes
    # def _search_conflicts_validate_error(self):
    #    pass

    # Default handler - this method should be overridden in extending Builder classes
    # def _search_conflicts_error(self):
    #    pass

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def check_words_requiring_consent(self, list_name, name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    # TODO: Ensure this isn't needed anywhere before replacing it!
    # @abc.abstractmethod
    #def check_designation(self, list_name, entity_type_user, all_designations, wrong_designation_place, misplaced_designation_any, misplaced_designation_end, all_designations_user):
    #    return ProcedureResult(is_valid=True)

    '''
        This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
        @return ProcedureResult
        '''

    @abc.abstractmethod
    def check_designation_mismatch(self, list_name, entity_type_user, all_designations, all_designations_user):
        return ProcedureResult(is_valid=True)

    '''
        This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
        @return ProcedureResult
        '''

    @abc.abstractmethod
    def check_designation_misplaced(self, list_name, misplaced_designation_any, misplaced_designation_end, misplaced_designation_all):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def check_word_special_use(self, list_name, name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''
    @abc.abstractmethod
    def get_most_similar_names(self, dict_highest_counter, dict_highest_detail, matches, list_dist, list_desc, list_name, name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''
    @abc.abstractmethod
    def get_details_most_similar(self, list_response, dist_substitution_dict, desc_substitution_dict):
        return ProcedureResult(is_valid=True)
