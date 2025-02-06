from claravy.taxonomy import *


class Parse_Trustlook:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK (TOK:TOK)": self.parse_delim_fmt2,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, PRE, FAM]

    # TOK.TOK.TOK (TOK:TOK)
    def parse_delim_fmt2(self, tokens):
        return [FILE, PRE, PRE, SUF, SUF, NULL]
