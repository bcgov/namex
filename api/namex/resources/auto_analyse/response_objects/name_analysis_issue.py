from . import Serializable


class NameAnalysisIssue(Serializable):
    def __init__(self, **kwargs):
        self.consentingBody = kwargs['consentingBody'] or None  # None <ConsentingBody>[]
        self.designations = kwargs['designations'] or None  # <string>[] | None
        self.descriptiveWords = kwargs['descriptiveWords'] or None  # <DescriptiveWord>[]
        # [add_descriptive | word_to_avoid | excess_words | consent_required | unclassified_word]
        self.issueType = kwargs['issueType'] or None  # <string> | None
        self.word = kwargs['word'] or None  # <string> | None
        self.wordIndex = kwargs['wordIndex'] or None  # <integer> | None
        self.showExaminationButton = kwargs['showExaminationButton'] or False  # <boolean>
        self.conflicts = kwargs['conflicts'] or None  # <Conflict>[] | None
        self.options = kwargs['options'] or None  # TODO: What is this shape?
        self.nameActions = kwargs['nameActions'] or None  # <NameAction>[] | None