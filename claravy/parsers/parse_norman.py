import re
from claravy.taxonomy import *


class Parse_Norman:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK_TOK.TOK": self.parse_delim_fmt3,
            "TOK/TOK_TOK.TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK": self.parse_delim_fmt6,
            "TOK.TOK!TOK": self.parse_delim_fmt7,
        }

    # TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [FAM, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF]

    # TOK_TOK.TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[0] == "Packed":
            tax = [PRE, PACK, SUF]
        elif tokens[1] == "Generic" or re.match(r"^Gen[0-9]*$", tokens[1]):
            tax = [PRE, SUF, SUF]
        elif len(tokens[1]) == 1 or tokens[1].islower():
            tax = [FAM, SUF, SUF]
        else:
            tax = [UNK, UNK, SUF] # Bad format
        return tax

    # TOK/TOK_TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if tokens[1] == "Packed":
            tax = [FILE, PRE, PACK, SUF]
        elif tokens[2] == "Generic" or re.match(r"^Gen[0-9]*$", tokens[1]):
            tax = [FILE, PRE, SUF, SUF]
        elif len(tokens[2]) == 1 or tokens[2].islower():
            tax = [FILE, FAM, SUF, SUF]
        else:
            tax = [FILE, UNK, UNK, SUF] # Bad format
        return tax

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK
    def parse_delim_fmt6(self, tokens):
        tax = [UNK]
        if tokens[0].isnumeric() or tokens[0].isupper():
            tax = [SUF]
        else:
            tax = [FAM]
        return tax

    # TOK.TOK!TOK
    def parse_delim_fmt7(self, tokens):
        return [FAM, SUF, SUF]
