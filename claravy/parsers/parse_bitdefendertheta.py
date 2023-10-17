from claravy.taxonomy import *


class Parse_Bitdefendertheta:

    def __init__(self):
        self.parse_fmt = {
            "TOK:TOK.TOK": self.parse_fmt1,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK@TOK!TOK": self.parse_fmt4,
            "TOK:TOK.TOK.TOK.TOK@TOK@TOK": self.parse_fmt5,
            "TOK:TOK.TOK.TOK": self.parse_fmt6,
            "TOK:TOK.TOK.TOK.@TOK@TOK": self.parse_fmt7,
            "TOK:TOK.TOK.TOK.TOK!TOK": self.parse_fmt8,
        }


    # TOK:TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, CAT, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK!TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK@TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK.@TOK@TOK
    def parse_fmt7(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK!TOK
    def parse_fmt8(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]
