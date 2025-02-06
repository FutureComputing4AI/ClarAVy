from claravy.taxonomy import *


class Parse_Crowdstrike:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK_TOK_TOK% (TOK)": self.parse_delim_fmt1,
            "TOK_TOK_TOK% (TOK)": self.parse_delim_fmt2,
        }

    # TOK/TOK_TOK_TOK%
    def parse_delim_fmt1(self, tokens):
        return [FILE, PRE, PRE, SUF, SUF, NULL]

    # TOK_TOK_TOK%
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, SUF, SUF, NULL]
