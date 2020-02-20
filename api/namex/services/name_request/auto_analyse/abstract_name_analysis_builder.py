import abc

from . import ProcedureResult


class AbstractNameAnalysisBuilder():
    __metaclass__ = abc.ABCMeta

    _director = None

    # Properties specific to this director implementation
    # TODO: Are these arrays or dicts?
    _synonyms = []
    _substitutions = []
    _stop_words = []
    _designated_end_words = []
    _designated_any_words = []

    _designation_any_list_user = []
    _designation_end_list_user = []

    _in_province_conflicts = []
    _all_conflicts = []

    _entity_type = None
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

    # TODO: Raise an exception if entity type is not set!!!
    # TODO: Validate entity types against valid types
    def get_entity_type(self):
        return self._entity_type

    def set_entity_type(self, entity_type):
        self._entity_type = entity_type

    def set_dicts(self, **kwargs):
        self._synonyms = kwargs.get('synonyms')
        self._substitutions = kwargs.get('substitutions')

        self._stop_words = kwargs.get('stop_words')
        self._designated_end_words = kwargs.get('designated_end_words')
        self._designated_any_words = kwargs.get('designated_any_words')

        self._designation_end_list_user = kwargs.get('designation_end_list_user')
        self._designation_any_list_user = kwargs.get('designation_any_list_user')

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

    def desc_synonym_list(self):
        return self._synonyms

    def get_substitution_list(self):
        return self._substitution_list

    def get_synonym_list(self, word):
        return self._synonym_list

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
        self._synonym_service = director.get_synonym_service()
        self._virtual_word_condition_service = director.get_virtual_word_condition_service()

    def get_synonym_service(self):
        return self._synonym_service

    def get_word_classification_service(self):
        return self._word_classification_service

    def get_virtual_word_condition_service(self):
        return self._virtual_word_condition_service

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

    @abc.abstractmethod
    def check_name_is_well_formed(self, list_dist, list_desc, list_none, company_name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def check_words_to_avoid(self):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def search_conflicts(self, list_dist, list_desc):
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
    def check_words_requiring_consent(self):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''

    @abc.abstractmethod
    def check_designation(self):
        return ProcedureResult(is_valid=True)
