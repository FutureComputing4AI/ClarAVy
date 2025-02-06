from claravy.taxonomy import *


class Parse_Bitdefendertheta:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK.TOK": self.parse_delim_fmt1,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK@TOK!TOK": self.parse_delim_fmt4,
            "TOK:TOK.TOK.TOK.TOK@TOK@TOK": self.parse_delim_fmt5,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK:TOK.TOK.TOK.@TOK@TOK": self.parse_delim_fmt7,
            "TOK:TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt8,
        }


    # TOK:TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, CAT, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK!TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK@TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK.@TOK@TOK
    def parse_delim_fmt7(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt8(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]
