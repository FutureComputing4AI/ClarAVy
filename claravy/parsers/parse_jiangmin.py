import re
from claravy.taxonomy import *


class Parse_Jiangmin:

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK": self.parse_fmt2,
            "TOK/TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK-TOK/TOK.TOK": self.parse_fmt5,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK, UNK]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            fmt = [PRE, VULN, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif tokens[2].islower() or tokens[2].isnumeric() or tokens[2].startswith("Gen"):
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, UNK, UNK]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].islower() or tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower() or tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK-TOK/TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [CAT, CAT, UNK, UNK]
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            fmt = [CAT, CAT, FAM, SUF]
        elif tokens[2].isupper():
            fmt = [CAT, CAT, PRE, FAM]
        else:
            fmt = [CAT, CAT, UNK, UNK] # Bad format
        return fmt
