from .name_analysis_utils import clean_name_words

class ProcedureResult:
    def __init__(self, **kwargs):
        self.is_valid = kwargs.get('is_valid', False)
        self.result_code = kwargs.get('result_code', None)
        self.values = kwargs.get('values', [])

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

    def set_name(self, **kwargs):
        self._name = kwargs.get('name')
        self._list_name_words = kwargs.get('list_name')
        self._list_dist_words = kwargs.get('list_dist')
        self._list_desc_words = kwargs.get('list_desc')
        self._list_none_words = kwargs.get('list_none')

    def set_dicts(self, **kwargs):
        self._synonyms = kwargs.get('synonyms')
        self._substitutions = kwargs.get('substitutions')

        self._stop_words = kwargs.get('stop_words')
        self._designated_end_words = kwargs.get('designated_end_words')
        self._designated_any_words = kwargs.get('designated_any_words')

        self._in_province_conflicts = kwargs.get('in_province_conflicts')
        self._all_conflicts = kwargs.get('all_conflicts')

    # API for extending implementations
    def get_name(self):
        return self._name

    def get_list_name(self):
        return self._list_name_words

    def get_list_dist(self):
        return self._list_dist_words

    def get_list_desc(self):
        return self._list_desc_words

    def get_list_none(self):
        return self._list_none_words

    def get_synonyms(self):
        return self._synonyms

    def get_substitutions(self):
        return self._substitutions

    def get_stop_words(self):
        return self._stop_words

    def get_designated_end_words(self):
        return self._designated_end_words

    def get_designated_any_words(self):
        return self._designated_any_words

    def __init__(self, director):
        # Store a reference to the director, we will need to access methods on the director instance to do things
        # like updating the classifications table
        self._director = director
        self._word_classification_service = director.get_word_classification_service()

    def get_word_classification_service(self):
        return self._word_classification_service

    # Just a wrapped call to the API's getClassification
    def get_word_classification(self, word):
        return self._word_classification_service.find_one(word)

    # Just a wrapped call to the API's updateClassification
    def update_word_classification(self, word_classification):
        return self._word_classification_service.update(word_classification)

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
