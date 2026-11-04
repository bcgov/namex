from synonyms.services import SynonymService

syn_svc = SynonymService()
all_designations = ["community contribution company", "limited liability partnership",
                    "unlimited liability company", "limited liability company", "limited liability co.",
                    "limited partnership", "co-operative", "incorporated", "corporation", "cooperative",
                    "liability", "company", "limited", "l.l.c.", "co-op", "corp.", "l.l.c", "corp", "ltd.", "coop",
                    "ulc.", "inc.", "ccc", "co.", "llc", "ulc", "ltd", "inc", "llp", "co"]
prefix_list = ["un", "re", "in", "dis", "en", "non", "in", "over", "mis", "sub", "pre", "inter", "fore", "de",
               "trans", "super", "semi", "anti", "mid", "under", "ante", "bene", "circum", "co", "com", "con",
               "col", "dia", "ex", "homo", "hyper", "mal", "micro", "multi", "para", "poly", "post", "pro", "retro",
               "tele", "therm", "trans", "uni"]
number_list = ["nine hundred", "one hundred", "eleventh", "eleven", "second", "three", "first", "third", "eight",
               "five", "nine", "one", "two"]
exceptions_ws = ["activ8", "h20"]

designation_all_regex = "(" + "|".join(all_designations) + ")"
prefixes = "|".join(prefix_list)
numbers = "|".join(number_list)
ordinal_suffixes = "ST|[RN]D|TH"
stand_alone_words = "HOLDINGS$|BC$|VENTURES$|SOLUTION$|ENTERPRISE$|INDUSTRIES$"
internet_domains = ".COM|.ORG|.NET|.EDU"
