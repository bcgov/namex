# Import mock API clients
from ..datasources.synonyms_api import SynonymsApi
from ..datasources.solr_api import SolrApi
from ..datasources.word_classification_api import WordClassificationApi


'''
This is the director for AutoAnalyseService
'''


class NameAnalysisDirector:
    _builder = None  # Store a reference to the builder
    _synonyms_api = None
    _solr_api = None
    _word_classification_api = None

    def __init__(self):
        self._word_classification_api = WordClassificationApi()
        self._synonyms_api = SynonymsApi()
        self._solr_api = SolrApi()

    def use_builder(self, builder):
        self._builder = builder if builder else None
        if self._builder:
            self.prepare_data()

    # Just a wrapped call to the builder's set_name method
    def set_name(self, name):
        self._builder.set_name(name)

    # Just a wrapped call to the builder's get_name method
    def get_name(self):
        return self._builder.get_name()

    # Prepare any data required by the analysis builder
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

    # This is the main execution call for the class
    def execute_analysis(self):
        raise NotImplementedError('execute_analysis must be implemented in extending classes')

    # Get the company's designation if it's in the name
    def get_name_designation(self):
        pass

    # Just a wrapped call to the API's getClassification
    def get_word_classification(self, word):
        return self._word_classification_api.get_word_classification(word)

    # Just a wrapped call to the API's updateClassification
    def update_word_classification(self, word):
        return self._word_classification_api.update_word_classification(word)


