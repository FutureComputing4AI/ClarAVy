import re
from claravy.taxonomy import *


class Parse_Ikarus:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK-TOK.TOK.TOK": self.parse_fmt3,
            "TOK-TOK.TOK": self.parse_fmt4,
            "TOK-TOK-TOK:TOK.TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK-TOK-TOK:TOK.TOK.TOK": self.parse_fmt7,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt8,
            "TOK-TOK": self.parse_fmt9,
            "TOK": self.parse_fmt10,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[0] == "Packer":
            if len(tokens[2]) == 1:
                fmt = [PRE, PACK, SUF]
            else:
                fmt = [PRE, PRE, PACK]
        if tokens[2].isnumeric() or re.match(r"^Gen[0-9]+$", tokens[2]):
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, UNK, UNK] # Bad format
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK
    def parse_fmt2(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) == 1:
            fmt = [FAM, SUF]
        elif re.match(r"^CVE[0-9]+$", tokens[1]):
            fmt = [PRE, VULN]
        else:
            fmt = [PRE, FAM]
        return fmt # Kind of messy format, but parsed ok

    # TOK-TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [UNK, UNK, UNK, UNK]
        if tokens[3].isupper():
            fmt = [PRE, PRE, UNK, UNK]
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF]
        else:
            fmt = [CAT, CAT, TGT, FAM]
        return fmt

    # TOK-TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [CAT, CAT, UNK]
        if tokens[2].isupper():
            fmt = [CAT, CAT, UNK]
        elif tokens[2].isnumeric() or re.match(r"^Gen[0-9]+$", tokens[2]):
            fmt = [CAT, CAT, SUF]
        else:
            fmt = [CAT, CAT, FAM]
        return fmt

    # TOK-TOK-TOK:TOK.TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, PRE, PRE, FAM] # Also kind of messy but parsed ok

    # TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [UNK, UNK, UNK, UNK]
        if tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3].islower():
            if (tokens[2].isupper() or len(tokens[2]) <= 2) and tokens[2] != "VB":
                fmt = [PRE, UNK, UNK, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, PRE, FAM, SUF]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, UNK, UNK] # Bad format
        elif tokens[3] == "Based":
            fmt = [PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM]
        return fmt

    # TOK-TOK-TOK:TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        return [PRE, PRE, PRE] + self.parse_fmt1(tokens[3:])

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        fmt = [UNK, UNK, UNK, UNK, SUF]
        if tokens[3].isupper() and tokens[3] != "VB":
            fmt = [PRE, PRE, UNK, UNK, SUF]
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [CAT, CAT, TGT, FAM, SUF]
        return fmt

    # TOK-TOK
    def parse_fmt9(self, tokens):
        if tokens[1].isnumeric():
            fmt = [FAM, SUF]
        elif tokens[0] in ["Tojan", "Trojan"]:
            fmt = [CAT, CAT]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK
    def parse_fmt10(self, tokens):
        return [FAM]
