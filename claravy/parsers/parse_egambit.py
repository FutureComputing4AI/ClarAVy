from claravy.taxonomy import *


class Parse_Egambit:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK_TOK_TOK%": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK": self.parse_delim_fmt3,
        }

    # TOK.TOK_TOK_TOK%
    def parse_delim_fmt1(self, tokens):
        return [PRE, PRE, PRE, SUF, NULL]

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM] # Very few families

    # TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, PRE, UNK]
        if tokens[0] != "PE":
            tax = [CAT, PRE, FAM]
        else:
            tax = [PRE, PRE, PRE]
        return tax
