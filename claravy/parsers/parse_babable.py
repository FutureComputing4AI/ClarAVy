from claravy.taxonomy import *


class Parse_Babable:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK": self.parse_fmt1,
        }

    # TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, SUF]
