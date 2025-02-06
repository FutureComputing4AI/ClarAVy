from claravy.taxonomy import *


class Parse_Panda:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK TOK": self.parse_delim_fmt2,
            "TOK/TOK": self.parse_delim_fmt3,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK": self.parse_delim_fmt5,
            "TOK": self.parse_delim_fmt6,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, SUF]
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [PRE, SUF, SUF]
        elif tokens[1].isupper():
            tax = [PRE, UNK, SUF] # Bad format
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE]

    # TOK/TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, FAM]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt5(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) <= 2 or tokens[1].lower() == "gen":
            if tokens[0].isupper():
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif tokens[1].isupper():
            if tokens[0].isnumeric():
                tax = [SUF, SUF]
            else:
                tax = [FAM, SUF]
        else:
            tax = [UNK, UNK] # Bad format
        return tax

    # TOK
    def parse_delim_fmt6(self, tokens):
        return [FAM]
