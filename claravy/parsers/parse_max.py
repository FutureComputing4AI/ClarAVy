from claravy.taxonomy import *


class Parse_Max:

    def __init__(self):
        self.parse_fmt = {
            "TOK (TOK TOK=TOK)": self.parse_fmt1,
        }

    # TOK (TOK TOK=TOK)
    def parse_fmt1(self, tokens):
        return [PRE, SUF, SUF, SUF, NULL]

