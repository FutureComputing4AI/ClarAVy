from claravy.taxonomy import *


class Parse_Babable:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK": self.parse_delim_fmt1,
        }

    # TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, SUF]
