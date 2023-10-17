import re
from claravy.taxonomy import *


class Parse_Ahnlabv3:

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_fmt2,
            "TOK/TOK": self.parse_fmt3,
            "TOK-TOK/TOK.TOK": self.parse_fmt4,
            "TOK-TOK/TOK.TOK.TOK": self.parse_fmt5,
            "TOK-TOK/TOK": self.parse_fmt6,
            "TOK/TOK.TOK_TOK.TOK": self.parse_fmt7,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt8,
            "TOK.TOK": self.parse_fmt9,
            "TOK-TOK.TOK": self.parse_fmt10,
            "TOK/TOK-TOK-TOK": self.parse_fmt11,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        if tokens[2].isupper() and len(tokens[2]) <= 3 and tokens[2] not in ["VB", "BHO", "WOW"]:
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isnumeric() or re.match(r"^Gen[0-9]*$", tokens[2]):
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].islower() or len(tokens[2]) == 1 or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK
    def parse_fmt3(self, tokens):
        return [PRE, FAM]

    # TOK-TOK/TOK.TOK
    def parse_fmt4(self, tokens):
        return [TGT, PRE, FAM, SUF]

    # TOK-TOK/TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        return [TGT, CAT, FAM, SUF, SUF]

    # TOK-TOK/TOK
    def parse_fmt6(self, tokens):
        return [TGT, CAT, FAM]

    # TOK/TOK.TOK_TOK.TOK
    def parse_fmt7(self, tokens):
        return [CAT, TGT, PRE, FAM, SUF]

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        fmt = [TGT, UNK, UNK, SUF, SUF]
        if tokens[3].isnumeric():
            fmt = [TGT, FAM, CAT, SUF, SUF]
        elif len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt9(self, tokens):
        # TODO: Inconsistent format
        return [UNK, UNK]

    # TOK-TOK.TOK
    def parse_fmt10(self, tokens):
        return [FAM, FAM, SUF]

    #TOK/TOK-TOK-TOK
    def parse_fmt11(self, tokens):
        return [PRE, VULN, VULN, VULN]
