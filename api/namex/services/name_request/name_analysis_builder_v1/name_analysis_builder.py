from namex.services.name_request.auto_analyse.abstract_name_analysis_builder \
    import AbstractNameAnalysisBuilder, ProcedureResult


'''
Sample builder
# TODO: What convention should we use? Nice to use _v<BuilderVersion> if it doesn't break PEP8
'''


class NameAnalysisBuilder(AbstractNameAnalysisBuilder):
    # These properties are inherited from the parent
    # The build director (eg. NameAnalysisDirector) populates these properties
    # as part of its prepare_data
    # _synonyms = []
    # _substitutions = []
    # _stop_words = []
    # _designated_end_words = []
    # _designated_any_words = []
    #
    # _in_province_conflicts = []
    # _all_conflicts = []
    #
    # _name = ''

    _distinctive_words = []
    _descriptive_words = []

    '''
    Check to see if a provided name is valid
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_name_is_well_formed(self):
        result = ProcedureResult()
        result.is_valid = True
        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_words_to_avoid(self):
        result = ProcedureResult()
        result.is_valid = True
        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def search_conflicts(self):
        result = ProcedureResult()
        result.is_valid = True
        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_words_requiring_consent(self):
        result = ProcedureResult()
        result.is_valid = True
        return result

    '''
    Override the abstract / base class method
    @return ProcedureResult
    '''
    def check_designation(self):
        result = ProcedureResult()
        result.is_valid = True
        return result

