from ..name_request.auto_analyse.name_analysis_utils import clean_name_words, data_frame_to_list


class NameProcessingService:
    _synonyms_api = None

    _prefixes = []
    _stop_words = []
    _designated_end_words = []
    _designated_any_words = []

    _name_as_submitted = ''
    _preprocessed_name = ''
    _list_name_words = []
    _list_dist_words = []
    _list_desc_words = []
    _list_none_words = []

    '''
    Prepare any data required to process the name.
    '''
    def prepare_data(self):
        # Query database for word designations
        self._stop_words = self._synonyms_api.get_stop_words()
        self._designated_end_words = self._synonyms_api.get_designated_end_words()
        self._designated_any_words = self._synonyms_api.get_designated_any_words()

    '''
    Split a name string into classifiable tokens. Called internally whenever set_name is invoked.
    @:param string:name
    '''
    def preprocess_name(self):
        if not self._name_as_submitted:
            return  # TODO: Should we throw an error or something?

        # Clean the provided name and tokenize the string
        # Identify stop words, any words and end words an store the lists to our director instance
        self._list_name_words = clean_name_words(
            self._name_as_submitted,
            self._stop_words,
            self._designated_any_words,
            self._designated_end_words,
            [],  # French words
            self._prefixes
        )

        # Store results to instance TODO: Don't delete this! Not sure how I am going to re-implement this yet...
        # self._list_name_words, self._list_desc_words, self._list_none_words = data_frame_to_list(cf)

        # Store clean, preprocessed name to instance
        self.set_preprocessed_name(' '.join(map(str, self.get_list_name())))

    def set_preprocessed_name(self, name):
        # Process the name
        self._preprocessed_name = name  # Store the user's submitted name string

    # API for extending implementations
    def get_preprocessed_name(self):
        return self._preprocessed_name

    def get_list_name(self):
        return self._list_name_words

    def get_list_dist(self):
        return self._list_dist_words

    def get_list_desc(self):
        return self._list_desc_words

    def get_list_none(self):
        return self._list_none_words
