from enum import Enum
from nltk.stem import PorterStemmer

porter = PorterStemmer()


# Modes
MODE_SYNS = "Syns"
MODE_SUBS = "Subs"
MODE_STOP = "Stop"

# Categories
dsg_end = "Designations_end"
dsg_any = "Designations_any"
stop_w = "Stop Words"


class DesignationPositionCodes(Enum):
    START = "start"
    END = "end"
    ANY = "any"


class LanguageCodes(Enum):
    ENG = "ENGLISH"
    FR = "FRENCH"
