import re
from claravy.taxonomy import *


class Parse_Maxsecure:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK-TOK-TOK:TOK.TOK.TOK": self.parse_fmt4,
            "TOK-TOK-TOK-TOK-TOK.TOK": self.parse_fmt5,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            fmt = [PRE, PRE, SUF, SUF]
        elif tokens[2] == "Heur":
            fmt = [PRE, UNK, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        if tokens[2].islower() or tokens[2].isupper() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            fmt = [PRE, FAM, SUF]
        elif re.match(r"^.*Gen[0-9]*$", tokens[2]) or tokens[2] == "Dam":
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        if tokens[:3] == ["Not", "a", "virus"]:
            fmt = [PRE, PRE, PRE, PRE, FAM]
        elif tokens[3].isnumeric():
            fmt = [CAT, TGT, FAM, SUF, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            fmt = [CAT, PRE, FAM, SUF, SUF]
        else:
            fmt = [CAT, PRE, TGT, FAM, SUF]
        return fmt

    # TOK-TOK-TOK:TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE, CAT, FAM, SUF]

    # TOK-TOK-TOK-TOK-TOK.TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, PRE, CAT, FAM, SUF]
