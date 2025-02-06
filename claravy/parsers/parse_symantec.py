from claravy.taxonomy import *


class Parse_Symantec:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK!TOK": self.parse_delim_fmt3,
            "TOK": self.parse_delim_fmt4,
            "TOK TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt7,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif tokens[2].isnumeric() or len(tokens[2]) <= 2 or tokens[2].isupper():
            if tokens[1].isupper():
                tax = [UNK, UNK, SUF] # Bad format
            else:
                tax = [PRE, FAM, SUF]
        else:
            tax = [UNK, UNK, UNK] # Bad format - may be able to parse more?
        return tax

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].isupper() or tokens[1].islower():
            if tokens[0].isupper():
                tax = [UNK, UNK] # Bad format
            else:
                tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK!TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, FAM, SUF]

    # TOK
    def parse_delim_fmt4(self, tokens):
        return [FAM]

    # TOK TOK
    def parse_delim_fmt5(self, tokens):
        # Either [CAT, CAT] or [FAM, FAM]
        return [UNK, UNK] # Bad format

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt6(self, tokens):
        return self.parse_delim_fmt1(tokens) + [SUF]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [UNK, UNK, UNK, UNK]
        if tokens[1].isnumeric():
            tax = [UNK, SUF, UNK, SUF] # Bad format
        elif tokens[0] == "Suspicious":
            tax = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric():
            if tokens[1].islower():
                tax = [UNK, SUF, SUF, SUF] # Bad format
            else:
                tax = [PRE, FAM, SUF, SUF] # Some of PRE are family-like? Unsure
        elif len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, UNK] # Last token either CAT or SUF
        elif tokens[0] == "Heur":
            tax = [PRE, PRE, SUF, SUF]
        elif tokens[2].isupper():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax
