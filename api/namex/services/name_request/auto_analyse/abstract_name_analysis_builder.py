class ProcedureResult:
    def __init__(self, **kwargs):
        self.is_valid = kwargs.get('is_valid', False)
        self.result_code = kwargs.get('result_code', None)


class AbstractNameAnalysisBuilder:
    _director = None

    # Properties specific to this director implementation
    # TODO: Are these arrays or dicts?
    _synonyms = []
    _substitutions = []
    _stop_words = []
    _designated_end_words = []
    _designated_any_words = []

    _in_province_conflicts = []
    _all_conflicts = []

    _name = ''
    _list_name_words = []
    _list_dist_words = []
    _list_desc_words = []
    _list_none_words = []

    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

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

        self._stop_words = kwargs.get('stop_words')
        self._designated_end_words = kwargs.get('designated_end_words')
        self._designated_any_words = kwargs.get('designated_any_words')

        self._in_province_conflicts = kwargs.get('in_province_conflicts')
        self._all_conflicts = kwargs.get('all_conflicts')

    def __init__(self, director):
        # Store a reference to the director, we will need to access methods on the director instance to do things
        # like updating the classifications table
        self._director = director

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
        raise NotImplementedError('Can not perform name analysis, do_analysis is not implemented!')

    '''
    Check to see if a provided name is valid
    @return ProcedureResult
    '''
    def check_name_is_well_formed(self, list_dist, list_desc, list_none, company_name):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''
    def check_words_to_avoid(self):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''
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
    def check_words_requiring_consent(self):
        return ProcedureResult(is_valid=True)

    '''
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    '''
    def check_designation(self):
        return ProcedureResult(is_valid=True)

    # Just a wrapped call to the director's getClassification
    # The director's getClassification could be linked to WordClassificationService
    def get_word_classification(self, word):
        return self._director.get_word_classification(word)

    # Just a wrapped call to the director's updateClassification
    # The director's updateClassification could be linked to WordClassificationService
    def update_word_classification(self):
        return self._director.update_word_classification()
