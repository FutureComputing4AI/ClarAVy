from claravy.taxonomy import *


class Parse_Sangfor:

    def __init__(self):
        self.parse_fmt = {
            "TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK-TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK-TOK": self.parse_fmt4,
            "TOK.TOK.TOK-TOK-TOK": self.parse_fmt5,
        }

    # TOK
    def parse_fmt1(self, tokens):
        return [PRE]

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [CAT, TGT, FAM, SUF]

    # TOK.TOK-TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [CAT, PRE, PRE, PRE, SUF] # Save token - don't think it's a family

    # TOK.TOK.TOK-TOK
    def parse_fmt4(self, tokens):
        return [TGT, CAT, FAM, SUF]

    # TOK.TOK.TOK-TOK-TOK
    def parse_fmt5(self, tokens):
        return [TGT, CAT, FAM, SUF, SUF] 
