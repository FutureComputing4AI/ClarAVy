from claravy.taxonomy import *


class Parse_Elastic:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK (TOK TOK)": self.parse_delim_fmt1,
            "TOK.TOK.TOK": self.parse_delim_fmt2,
        }

    # TOK (TOK TOK)
    def parse_delim_fmt1(self, tokens):
        return [PRE, SUF, SUF, NULL]

    # TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, CAT, FAM]
