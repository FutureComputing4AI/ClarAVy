import re
from claravy.taxonomy import *


class Parse_Norman:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK": self.parse_fmt2,
            "TOK_TOK.TOK": self.parse_fmt3,
            "TOK/TOK_TOK.TOK": self.parse_fmt4,
            "TOK/TOK.TOK!TOK": self.parse_fmt5,
            "TOK": self.parse_fmt6,
            "TOK.TOK!TOK": self.parse_fmt7,
        }

    # TOK.TOK
    def parse_fmt1(self, tokens):
        return [FAM, SUF]

    # TOK/TOK.TOK
    def parse_fmt2(self, tokens):
        return [TGT, FAM, SUF]

    # TOK_TOK.TOK
    def parse_fmt3(self, tokens):
        if tokens[0] == "Packed":
            fmt = [PRE, PACK, SUF]
        elif tokens[1] == "Generic" or re.match(r"^Gen[0-9]*$", tokens[1]):
            fmt = [PRE, SUF, SUF]
        elif len(tokens[1]) == 1 or tokens[1].islower():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [UNK, UNK, SUF] # Bad format
        return fmt

    # TOK/TOK_TOK.TOK
    def parse_fmt4(self, tokens):
        if tokens[1] == "Packed":
            fmt = [TGT, PRE, PACK, SUF]
        elif tokens[2] == "Generic" or re.match(r"^Gen[0-9]*$", tokens[1]):
            fmt = [TGT, PRE, SUF, SUF]
        elif len(tokens[2]) == 1 or tokens[2].islower():
            fmt = [TGT, FAM, SUF, SUF]
        else:
            fmt = [TGT, UNK, UNK, SUF] # Bad format
        return fmt

    # TOK/TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK
    def parse_fmt6(self, tokens):
        fmt = [UNK]
        if tokens[0].isnumeric() or tokens[0].isupper():
            fmt = [SUF]
        else:
            fmt = [FAM]
        return fmt

    # TOK.TOK!TOK
    def parse_fmt7(self, tokens):
        return [FAM, SUF, SUF]
