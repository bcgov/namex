from namex.services.name_request.auto_analyse.name_analysis_utils import clean_name_words

# Import mock API clients
from ..mock_api_clients.synonyms_api_client import SynonymsApiClient
from ..mock_api_clients.solr_api_client import SolrApiClient
from ..mock_api_clients.word_classification_api_client import WordClassificationApiClient


'''
This is the director for AutoAnalyseService
'''


class NameAnalysisDirector:
    _builder = None  # Store a reference to the builder
    _synonyms_api = None
    _solr_api = None
    _word_classification_api = None

    # Properties specific to this director implementation
    # TODO: Are these arrays or dicts?
    _synonyms = []
    _substitutions = []
    _stop_words = []
    _designated_end_words = []
    _designated_any_words = []

    _in_province_conflicts = []
    _all_conflicts = []

    def __init__(self, builder):
        self.use_builder(builder)
        self._word_classification_api = WordClassificationApiClient()
        self._synonyms_api = SynonymsApiClient()
        self._solr_api = SolrApiClient()

    def use_builder(self, builder):
        self._builder = builder if builder else None
        if self._builder:
            self.prepare_data()

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

        # Store query results to instance
        self._synonyms = synonyms
        self._substitutions = substitutions

        self._stop_words = stop_words['synonyms_text'][0].split(',')
        self._designated_end_words = designated_end_words['synonyms_text'][0].split(',')
        self._designated_any_words = designated_any_words['synonyms_text'][0].split(',')

        self._in_province_conflicts = in_province_conflicts
        self._all_conflicts = all_conflicts

        self._builder.set_dicts(
            _synonyms=synonyms,
            _substitutions=substitutions,
            _stop_words=stop_words['synonyms_text'][0].split(','),
            _designated_end_words=designated_end_words['synonyms_text'][0].split(','),
            _designated_any_words=designated_any_words['synonyms_text'][0].split(','),
            _in_province_conflicts=in_province_conflicts,
            _all_conflicts=all_conflicts
        )

    # This is the main execution call for the class
    def execute_analysis(self):
        self.preprocess_name()
        self._builder.do_analysis()

    # Get the company's designation if it's in the name
    def get_name_designation(self):
        pass

    def preprocess_name(self, row):
        words = row.lower()
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

    # Just a wrapped call to the API's getClassification
    def get_word_classification(self, word):
        return self._word_classification_api.get_word_classification(word)

    # Just a wrapped call to the API's updateClassification
    def update_word_classification(self, word):
        return self._word_classification_api.update_word_classification(word)


