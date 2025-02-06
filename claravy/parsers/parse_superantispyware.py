from claravy.taxonomy import *


class Parse_Superantispyware:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK/TOK-TOK": self.parse_delim_fmt1,
            "TOK.TOK/TOK": self.parse_delim_fmt2,
            "TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK/TOK-TOK[TOK]": self.parse_delim_fmt4,
        }

    # TOK.TOK/TOK-TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[2] == "Gen":
            tax = [CAT, PRE, PRE, FAM]
        else:
            tax = [CAT, UNK, UNK, UNK] # Bad format
        return tax

    # TOK.TOK/TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [CAT, FAM]

    # TOK.TOK/TOK-TOK[TOK]
    def parse_delim_fmt4(self, tokens):
        if tokens[2] == "Gen":
            if tokens[4].isnumeric() or tokens[4].islower() or tokens[4].isupper():
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, UNK, UNK, SUF]
        else:
            tax = [PRE, UNK, PRE, UNK, SUF, NULL] # Bad format
        return tax
