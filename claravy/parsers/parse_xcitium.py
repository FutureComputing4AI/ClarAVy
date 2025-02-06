from claravy.taxonomy import *


class Parse_Xcitium:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK@TOK": self.parse_delim_fmt3,
            "TOK@#TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.~TOK@TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.~TOK@TOK": self.parse_delim_fmt6,
        }

    # TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt1(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, FILE, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK@TOK
    def parse_delim_fmt3(self, tokens):
        return [UNK, UNK, UNK, SUF] # Bad format

    # TOK@#TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, SUF]

    # TOK.TOK.TOK.~TOK@TOK
    def parse_delim_fmt5(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.~TOK@TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, FILE, CAT, FAM, SUF, SUF]
