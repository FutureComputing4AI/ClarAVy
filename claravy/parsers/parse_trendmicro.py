import re
from claravy.taxonomy import *


class Parse_Trendmicro: # Same company as Trendmicrohousecall

    def __init__(self):
        self.parse_fmt = {
            "TOK_TOK.TOK": self.parse_fmt1,
            "TOK_TOK_TOK.TOK": self.parse_fmt2,
            "TOK_TOK.TOK-TOK": self.parse_fmt3,
            "TOK_TOK-TOK": self.parse_fmt4,
            "TOK_TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK": self.parse_fmt6,
        }

    # TOK_TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, SUF]
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [PRE, SUF, SUF]
        elif len(tokens[1]) == 3:
            fmt = [UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK_TOK_TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, SUF, SUF]
        if len(tokens[1]) <= 3:
            fmt = [PRE, UNK, SUF, SUF] # Bad format
        else:
            fmt = [PRE, FAM, SUF, SUF]
        return fmt

    # TOK_TOK.TOK-TOK
    def parse_fmt3(self, tokens):
        return [PRE, FAM, SUF, SUF]

    # TOK_TOK-TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, SUF]
        if re.match(r"CVE[0-9]+", tokens[1]):
            fmt = [PRE, VULN, SUF]
        elif len(tokens[1]) <= 4:
            fmt = [PRE, UNK, SUF] # Bad format
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK_TOK
    def parse_fmt5(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].islower():
            fmt = [UNK, SUF] # Bad format
        elif len(tokens[1]) <= 3:
            fmt = [PRE, UNK] # Bad format
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [CAT, TGT, FAM, SUF]
