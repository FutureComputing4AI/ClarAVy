from claravy.taxonomy import *


class Parse_Zoner:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[2].isnumeric():
            tax = [CAT, FILE, SUF]
        elif tokens[2].isupper() and tokens[1] != "VB":
            if tokens[1].isupper():
                tax = [CAT, FILE, SUF]
            else:
                tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, UNK, UNK] # Bad format
        return tax

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [CAT, UNK, UNK, SUF]
        if tokens[3].isnumeric():
            tax = [CAT, FILE, FAM, SUF]
        else:
            tax = [CAT, UNK, UNK, SUF] # Bad format
        return tax
