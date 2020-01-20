from .auto_analyse.get_conflicts_proc import get_conflicts
from .auto_analyse.get_words_req_consent_proc import get_words_req_consent
from .auto_analyse.get_words_to_avoid_proc import get_words_to_avoid

class AutoAnalyseService:
    def __init__(self):
        pass

    def executeAnalysis(self):
        self.cleanName()
        self.validateName()
        # TODO: Loop over words, call getWordClassification
        pass

    # Sanitize input and clean the provided name
    def cleanName(self):
        pass

    # Get the classification for a specific word
    def getWordClassification(self):
        pass

    # Get the company's designation if it's in the name
    def getNameDesignation(self):
        pass

    # Validate the name
    def validateName(self):
        self.validateNameIsWellFormed()

    # Check to see if a provided name is valid
    def validateNameIsWellFormed(self):
        pass

