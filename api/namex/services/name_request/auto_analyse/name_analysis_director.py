from namex.models import Synonym

from .mixins.get_synonyms_lists import GetSynonymsListsMixin
from .mixins.get_designations_lists import GetDesignationsListsMixin
from .mixins.get_word_classification_lists import GetWordClassificationListsMixin

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
    # Name + tokens
    _entity_type = None
    _name_as_submitted = ''
    _preprocessed_name = ''

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

    def __init__(self):
        self.synonym_service = SynonymService()
        self.word_classification_service = WordClassificationService()
        self.word_condition_service = VirtualWordConditionService()
        self.name_processing_service = NameProcessingService()
        self.builder = None

    def use_builder(self, builder):
        self.builder = builder if builder else None

    # API for extending implementations
    def get_name(self):
        return self._name_as_submitted

    # API for extending implementations
    def get_preprocessed_name(self):
        return self._preprocessed_name

    # Get the company's designation if it's in the name
    def get_name_designation(self):
        pass

    # API for extending implementations
    def get_entity_type(self):
        # TODO: Raise an exception if entity type is not set!!!
        # TODO: Validate entity types against valid types
        return self._entity_type

    def set_entity_type(self, entity_type):
        self._entity_type = entity_type

    '''
    Set and preprocess a submitted name string using the preprocess_name class method.
    '''
    def set_name(self, name):
        np_svc = self.name_processing_service
        wc_svc = self.word_classification_service

        self._name_as_submitted = name  # Store the user's submitted name string

        np_svc.set_name(name)  # Setting the name will automatically clean the name
        # Store the clean, processed name to our director instance
        self._preprocessed_name = np_svc.processed_name
        self._list_name_words = np_svc.name_tokens

        # Classify the tokens that were created by NameProcessingService
        token_classifier = wc_svc.classify_tokens(np_svc.name_tokens)

        # Store the classified tokens to our director instance
        self._list_dist_words, self._list_desc_words, self._list_none_words = [
            token_classifier.distinctive_word_tokens,
            token_classifier.descriptive_word_tokens,
            token_classifier.unclassified_word_tokens
        ]

        self.configure_builder()  # Update builder dicts

    '''
    Prepare any data required by the analysis builder.
    prepare_data is an abstract method and must be implemented in extending classes.
    '''
    def prepare_data(self):
        syn_svc = self.synonym_service

        # Query database for synonyms, substitutions and designations
        self._synonyms = syn_svc.get_synonyms()
        self._substitutions = syn_svc.get_substitutions()
        self._prefixes = syn_svc.get_prefixes()

        self._stop_words = syn_svc.get_stop_words()
        self._designated_end_words = syn_svc.get_designated_end_all_words()
        self._designated_any_words = syn_svc.get_designated_any_all_words()

        self.configure_builder()

    def configure_builder(self):
        self.builder.set_entity_type(self._entity_type)
        self.builder.set_dicts(
            # List of all synonyms, loaded into the director in prepare_data
            synonyms=self._synonyms,
            # List of all substitution, loaded into the director in prepare_data
            substitutions=self._substitutions,
            stop_words=self._stop_words,
            designated_end_words=self._designated_end_words,
            designated_any_words=self._designated_any_words,
            designation_end_list_user=self._designation_end_list_user,
            designation_any_list_user=self._designation_any_list_user,
            entity_end_designation_dict=self._entity_end_designation_dict,
            entity_any_designation_dict=self._entity_any_designation_dict
        )

    '''
    This is the main execution call that wraps name analysis checks. 
    - Perform checks to ensure the name is well formed. 
    - If the name is well formed, proceed with our analysis by calling do_analysis.
    - If you don't want to check to see if a name is well formed first, override check_name_is_well_formed in the supplied builder.
    @:return ProcedureResult[]
    '''
    def execute_analysis(self):
        builder = self.builder

        results = []
        if self.get_list_none():
            self._list_dist_words, self._list_desc_words = TokenClassifier.handle_unclassified_words(
                self.get_list_dist(),
                self.get_list_desc(),
                self.get_list_none(),
                self.get_list_name()
            )

        check_name_is_well_formed = builder.check_name_is_well_formed(
            self.get_list_dist(),
            self.get_list_desc(),
            self.get_list_none(),
            self.get_list_name()
        )

        if not check_name_is_well_formed.is_valid:
            results.append(check_name_is_well_formed)
            return results
            #  Do not continue

        # TODO: Persist preprocessed name here?
        return results + self.do_analysis()

    '''
    This is the main execution call for running name analysis checks.
    do_analysis is an abstract method and must be implemented in extending classes.
    @:return ProcedureResult[]
    '''
    def do_analysis(self):
        raise NotImplementedError('do_analysis must be implemented in extending classes')
