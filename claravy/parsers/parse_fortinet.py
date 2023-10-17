import re
from claravy.taxonomy import *


class Parse_Fortinet:

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK!TOK": self.parse_fmt1,
            "TOK/TOK": self.parse_fmt2,
            "TOK/TOK.TOK": self.parse_fmt3,
            "TOK/TOK.TOK!TOK.TOK": self.parse_fmt4,
            "TOK/TOK.TOK.TOK!TOK": self.parse_fmt5,
            "TOK/TOK!TOK": self.parse_fmt6,
            "TOK": self.parse_fmt7,
            "TOK/TOK.TOK.TOK": self.parse_fmt8,
            "TOK/TOK.TOK@TOK": self.parse_fmt9,
            "TOK/TOK_TOK": self.parse_fmt10,
        }

    # TOK/TOK.TOK!TOK
    def parse_fmt1(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK/TOK
    def parse_fmt2(self, tokens):
        return [PRE, FAM]

    # TOK/TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, SUF]
        if re.match(r"CVE[0-9]+", tokens[2]):
            fmt = [PRE, UNK, VULN]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK!TOK.TOK
    def parse_fmt4(self, tokens):
        return [TGT, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        fmt = [TGT, UNK, UNK, SUF, SUF]
        if re.match(r"CVE[0-9]+", tokens[2]):
            fmt = [TGT, PRE, VULN, SUF, SUF]
        elif tokens[1] == "Generic":
            fmt = [TGT, PRE, SUF, SUF, SUF]
        else:
            fmt = [TGT, UNK, UNK, SUF, SUF]
        return fmt

    # TOK/TOK!TOK
    def parse_fmt6(self, tokens):
        fmt = [PRE, FAM, UNK]
        if tokens[2].islower() or tokens[2].isupper() or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, FAM, UNK] # Weird format - Morphine, Monder?
        return fmt

    # TOK
    def parse_fmt7(self, tokens):
        return [FAM]

    # TOK/TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        if tokens[2].isupper() or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK!TOK
    def parse_fmt9(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK/TOK_TOK
    def parse_fmt10(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[2].isnumeric() or tokens[2].islower() or tokens[2].isupper():
            if tokens[1].isupper():
                fmt = [PRE, UNK, SUF] # Bad format
            else:
                fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt
