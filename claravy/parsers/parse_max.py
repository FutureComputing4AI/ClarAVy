from claravy.taxonomy import *


class Parse_Max:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK (TOK TOK=TOK)": self.parse_delim_fmt1,
        }

    # TOK (TOK TOK=TOK)
    def parse_delim_fmt1(self, tokens):
        return [PRE, SUF, SUF, SUF, NULL]

