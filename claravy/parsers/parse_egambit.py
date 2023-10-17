from claravy.taxonomy import *


class Parse_Egambit:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK_TOK_TOK%": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK": self.parse_fmt3,
        }

    # TOK.TOK_TOK_TOK%
    def parse_fmt1(self, tokens):
        return [PRE, PRE, PRE, SUF, NULL]

    # TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, FAM] # Very few families

    # TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [UNK, PRE, UNK]
        if tokens[0] != "PE":
            fmt = [CAT, PRE, FAM]
        else:
            fmt = [PRE, PRE, PRE]
        return fmt
