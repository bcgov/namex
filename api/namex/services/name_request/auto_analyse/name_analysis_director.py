# Import mock API clients
from ..datasources.synonyms_api import SynonymsApi
from ..datasources.solr_api import SolrApi
from ..datasources.word_classification_api import WordClassificationApi

from . import AnalysisIssueCodes

from namex.services.synonyms.synonym \
    import SynonymService

from namex.services.name_processing.name_processing \
    import NameProcessingService

from namex.services.word_classification.word_classification \
    import WordClassificationService

from namex.services.word_classification.token_classifier \
    import TokenClassifier

from namex.services.virtual_word_condition.virtual_word_condition \
    import VirtualWordConditionService

'''
This is the director for AutoAnalyseService.
'''


class NameAnalysisDirector(GetSynonymsListsMixin, GetDesignationsListsMixin, GetWordClassificationListsMixin):
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
    def name_processing_service(self):
        return self._name_processing_service

    @name_processing_service.setter
    def name_processing_service(self, svc):
        self._name_processing_service = svc

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    @property
    def model(self):
        return Synonym

    @property
    def entity_type(self):
        return self._entity_type

    def __init__(self):
        self._word_classification_api = WordClassificationApi()
        self._synonyms_api = SynonymsApi()
        self._solr_api = SolrApi()

        self.entity_type = None

    # Call this method from whatever is using this director
    def use_builder(self, builder):
        self.builder = builder if builder else None

    # Convenience method for extending implementations
    def get_entity_type(self):
        return self.entity_type

    # Convenience method for extending implementations
    def set_entity_type(self, entity_type):
        self.entity_type = entity_type

    # API for extending implementations
    def get_name_tokens(self):
        return self.name_tokens

    # API for extending implementations
    # TODO: Just for backward compat. et rid of this when we are done refactoring!
    def get_name(self):
        return self.name_tokens

    # API for extending implementations
    def get_original_name(self):
        return self.original_name

    # API for extending implementations
    def get_processed_name(self):
        return self.processed_name

    def get_original_name_tokenized(self):
        return self.original_name_tokenized

    '''
    Set and preprocess a submitted name string.
    Setting the name using np_svc.set_name will clean the name and set the following properties:
    @:prop name_as_submitted The original name string
    @:prop processed_name The cleaned name
    @:prop name_tokens Word tokens generated from the cleaned name
    '''
    def set_name(self, name):
        np_svc = self.name_processing_service
        wc_svc = self.word_classification_service

        np_svc.set_name(name)
        np_svc.set_name_tokenized(name)

        # TODO: Get rid of this when done refactoring!
        self._list_name_words = np_svc.name_tokens

        # Classify the tokens that were created by NameProcessingService
        self.token_classifier = wc_svc.classify_tokens(np_svc.name_tokens)

        self.configure_builder()

    '''
    Prepare any data required by the analysis builder.
    prepare_data is an abstract method and must be implemented in extending classes.
    '''
    def prepare_data(self):
        # Query database for synonyms, substitutions and designations
        synonyms = self._synonyms_api.get_synonyms()
        substitutions = self._synonyms_api.get_substitutions()

        stop_words = self._synonyms_api.get_stop_words()
        designated_end_words = self._synonyms_api.get_designated_end_words()
        designated_any_words = self._synonyms_api.get_designated_any_words()

        # Solr calls
        in_province_conflicts = self._solr_api.get_in_province_conflicts()
        all_conflicts = self._solr_api.get_all_conflicts()

        self._builder.set_dicts(
            synonyms=synonyms,
            substitutions=substitutions,
            stop_words=stop_words,
            designated_end_words=designated_end_words,
            designated_any_words=designated_any_words,
            in_province_conflicts=in_province_conflicts,
            all_conflicts=all_conflicts
        )

    '''
    This is the main execution call that wraps name analysis checks. 
    - Perform checks to ensure the name is well formed. 
    - If the name is well formed, proceed with our analysis by calling do_analysis.
    - If you don't want to check to see if a name is well formed first, override check_name_is_well_formed in the supplied builder.
    @:return ProcedureResult[]
    '''
    def execute_analysis(self):
        raise NotImplementedError('execute_analysis must be implemented in extending classes')

            list_name = self.name_tokens
            list_dist, list_desc, list_none = self.word_classification_tokens

            analysis = []
            if list_none and list_none.__len__() > 0:
                self._list_dist_words, self._list_desc_words = TokenClassifier.handle_unclassified_words(
                    list_dist,
                    list_desc,
                    list_none,
                    list_name
                )

            check_words_to_avoid = builder.check_words_to_avoid(list_name, self.processed_name)
            if not check_words_to_avoid.is_valid:
                analysis.append(check_words_to_avoid)
                return analysis

            check_name_is_well_formed = builder.check_name_is_well_formed(
                self.token_classifier.distinctive_word_tokens,
                self.token_classifier.descriptive_word_tokens,
                self.token_classifier.unclassified_word_tokens,
                self.name_tokens,
                self.name_original_tokens
            )

            analysis = analysis + check_name_is_well_formed

            # If the error coming back is that a name is not well formed
            # OR if the error coming back has words to avoid...
            # eg. result.result_code = AnalysisIssueCodes.CONTAINS_UNCLASSIFIABLE_WORD
            # don't return the result yet, the name is well formed, we just have an unclassified
            # word in the result.

            issues_that_must_be_fixed = [
                AnalysisIssueCodes.WORDS_TO_AVOID,
                AnalysisIssueCodes.TOO_MANY_WORDS,
                AnalysisIssueCodes.ADD_DISTINCTIVE_WORD,
                AnalysisIssueCodes.ADD_DESCRIPTIVE_WORD
            ]

    # Just a wrapped call to the API's getClassification
    def get_word_classification(self, word):
        return self._word_classification_api.get_word_classification(word)

        return word_issues

    @classmethod
    def _has_analysis_issue_type(cls, analysis, issue_code):
        return cls._get_analysis_issue_type_issues(analysis, issue_code).__len__() > 0

    @classmethod
    def _get_analysis_issue_type_issues(cls, analysis, issue_code):
        issues = list(
            filter(lambda i: i.result_code == issue_code, analysis)
        )

        return issues

    '''
    This is the main execution call for running name analysis checks.
    do_analysis is an abstract method and must be implemented in extending classes.
    @:return ProcedureResult[]
    '''
    def do_analysis(self):
        raise NotImplementedError('do_analysis must be implemented in extending classes')
