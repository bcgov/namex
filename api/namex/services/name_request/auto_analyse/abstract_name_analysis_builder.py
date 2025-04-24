import abc

from . import ProcedureResult
from .mixins.get_designations_lists import GetDesignationsListsMixin
from .mixins.get_synonyms_lists import GetSynonymsListsMixin
from .mixins.get_word_classification_lists import GetWordClassificationListsMixin


class AbstractNameAnalysisBuilder(GetSynonymsListsMixin, GetDesignationsListsMixin, GetWordClassificationListsMixin):
    __metaclass__ = abc.ABCMeta

    @property
    def director(self):
        return self._director

    @director.setter
    def director(self, director):
        self._director = director

    @property
    def name_processing_service(self):
        return self._name_processing_service

    @name_processing_service.setter
    def name_processing_service(self, svc):
        self._name_processing_service = svc

    @property
    def word_classification_service(self):
        return self._word_classification_service

    @word_classification_service.setter
    def word_classification_service(self, svc):
        self._word_classification_service = svc

    @property
    def word_condition_service(self):
        return self._word_condition_service

    @word_condition_service.setter
    def word_condition_service(self, svc):
        self._word_condition_service = svc

    @property
    def synonym_service(self):
        return self._synonym_service

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

    """
    Check to see if a provided name is valid
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_name_is_well_formed(self, dict_name, list_dist, list_desc, list_none, list_name, list_original_name):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    
    The reason this check is done separately from check_name_is_well_formed is
    because out of province / intl names may not follow the same analysis rules.
    Having this check separate allows us the flexibility of checking for words
    to avoid specifically in cases where it is necessary.
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_words_to_avoid(self, list_name, name):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def search_conflicts(self, list_dist, list_desc, list_name, name, check_name_is_well_formed, queue):
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

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_words_requiring_consent(self, list_name, name):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_designation_mismatch(self, list_name, entity_type_user, all_designations, all_designations_user):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_end_designation_more_than_once(
        self, list_name, all_designation_end_list, correct_designations_user, misplaced_designation_end
    ):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_designation_misplaced(self, list_name, misplaced_designation_end):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_designation_existence(self, list_name, all_designations, all_designations_user):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_word_special_use(self, list_name, name):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def get_most_similar_names(self, dict_highest_counter, matches, list_dist, list_desc, list_name):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def get_details_most_similar(self, list_response, dist_substitution_dict, desc_substitution_dict):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_word_limit(self, list_name):
        return ProcedureResult(is_valid=True)

    """
    This method IS abstract and MUST BE IMPLEMENTED in extending Builder classes
    @return ProcedureResult
    """

    @abc.abstractmethod
    def check_unclassified_words(self, list_name, list_none):
        return ProcedureResult(is_valid=True)
