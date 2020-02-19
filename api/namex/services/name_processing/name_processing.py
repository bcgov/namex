from ..name_request.auto_analyse.name_analysis_utils import remove_french, data_frame_to_list

from namex.services.synonyms.synonym \
    import SynonymService


# TODO: A mixin for some shared access methods wouldn't hurt...
class NameProcessingService:
    _synonym_service = None

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

    # TODO: Add kwargs so we can provide data as params if we've already loaded up the lists that we need!
    def __init__(self):
        self._synonym_service = SynonymService()
        self.prepare_data()

    '''
    Prepare any data required to process the name. Called internally when creating a new instance of this class.
    '''
    def prepare_data(self):
        # Query database for word designations
        self._stop_words = self._synonym_service.get_stop_words()
        #self._designated_end_words = self._synonym_service.get_designated_end_words()
        #self._designated_any_words = self._synonym_service.get_designated_any_words()
        self._designated_end_words = self._synonym_service.get_designated_end_all_words()
        self._designated_any_words = self._synonym_service.get_designated_any_all_words()

    '''
    Split a name string into classifiable tokens. Called internally whenever set_name is invoked.
    @:param string:name
    '''
    def preprocess_name(self):
        if not self._name_as_submitted:
            return  # TODO: Should we throw an error or something?

        # Clean the provided name and tokenize the string
        # Identify stop words, any words and end words an store the lists to our director instance
        self._list_name_words = self.clean_name_words(
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

    def clean_name_words(self, text, stop_words=[], designation_any=[], designation_end=[], fr_designation_end_list=[], prefix_list=[]):
        # TODO: Warn or something if params aren't set!
        words = text.lower()
        words = ' '.join([word for x, word in enumerate(words.split(" ")) if x == 0 or word not in stop_words])
        words = remove_french(words, fr_designation_end_list)
        tokens = self._synonym_service.regex_transform(words, designation_any, designation_end, prefix_list)
        tokens = tokens.split()

        return [x.lower() for x in tokens if x]

    '''
    Set and preprocess a submitted name string using the preprocess_name class method.
    '''
    def set_name(self, name):
        # Process the name
        self._name_as_submitted = name  # Store the user's submitted name string
        self.preprocess_name()

    # API for extending implementations
    def get_name(self):
        return self._name_as_submitted

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
