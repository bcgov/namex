from .auto_analyse.get_conflicts_proc import get_conflicts
from .auto_analyse.get_words_req_consent_proc import get_words_req_consent
from .auto_analyse.get_words_to_avoid_proc import get_words_to_avoid

class AutoAnalyseService:
    def __init__(self):
        pass

    def execute_analysis(self):
        self.clean_name()
        self.validate_name()
        # TODO: Loop over words, call getWordClassification
        pass

    # Sanitize input and clean the provided name
    def clean_name(self):
        pass

    # Get the classification for a specific word
    def get_word_classification(self):
        pass

    # Get the company's designation if it's in the name
    def get_name_designation(self):
        pass

    # Validate the name
    def validate_name(self):
        self.validate_name_is_well_formed()

    # Check to see if a provided name is valid
    def validate_name_is_well_formed(self):
        pass

