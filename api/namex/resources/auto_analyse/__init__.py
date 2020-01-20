from flask import json


class Serializable:
    def to_json(self):
        return json.dumps(self,
              separators=(',', ':'),
              default=lambda o: o.__dict__,
              sort_keys=True, indent=0).replace('\n', '')


# TODO: All the classes in here need a to_json method
class ConsentingBody(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs['name'] or ''  # Required! <string>
        self.email = kwargs['email'] or None  # <string> | None


class NameAction(Serializable):
    def __init__(self, **kwargs):
        self.type = kwargs['type'] or ''  # Required! [strike | add_word_brackets | highlight]
        self.position = kwargs['position'] or None  # [start | end] (is there another?)
        self.message = kwargs['message'] or None  # <string> | None


class DescriptiveWord(Serializable):
    def __init__(self, **kwargs):
        self.category = kwargs['category'] or ''  # Required! <string>
        self.wordList = kwargs['wordList'] or None  # <string>[] | None


class Conflict(Serializable):
    def __init__(self, **kwargs):
        self.name = kwargs['name'] or ''  # Required! <string>
        self.date = kwargs['date'] or None  # <date> | None


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


class NameAnalysisResponse(Serializable):
    def __init__(self, **kwargs):
        self.status = kwargs['status'] or ''
        self.issues = kwargs['issues'] or []