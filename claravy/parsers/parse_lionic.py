from claravy.taxonomy import *


class Parse_Lionic:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt5,
        }

    # TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3].islower() or tokens[3].isnumeric() or len(tokens[3]) == 1:
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 3:
            tax = [PRE, UNK, UNK, SUF] # Bad format
        elif tokens[2].startswith("Gen"):
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if len(tokens[2]) == 4 and tokens[2][0].islower():
            if tokens[1].startswith("Gen"):
                tax = [PRE, PRE, SUF]
            else:
                tax = [PRE, FAM, SUF]
        elif tokens[2].startswith("Gen"):
            tax = [PRE, PRE, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF, SUF]
        if tokens[4].isnumeric():
            tax = [PRE, PRE, UNK, UNK, SUF, SUF] # Bad format
        elif tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        return tax
