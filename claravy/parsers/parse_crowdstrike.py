from claravy.taxonomy import *


class Parse_Crowdstrike:

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK_TOK_TOK% (TOK)": self.parse_fmt1,
            "TOK_TOK_TOK% (TOK)": self.parse_fmt2,
        }

    # TOK/TOK_TOK_TOK%
    def parse_fmt1(self, tokens):
        return [TGT, PRE, PRE, SUF, SUF, NULL]

    # TOK_TOK_TOK%
    def parse_fmt2(self, tokens):
        return [PRE, PRE, SUF, SUF, NULL]
