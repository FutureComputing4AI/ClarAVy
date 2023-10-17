from claravy.taxonomy import *


class Parse_Kaspersky: # Partnership with Zonealarm

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK-TOK-TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK-TOK-TOK:TOK:TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK-TOK-TOK:TOK:TOK.TOK.TOK": self.parse_fmt7,
            "TOK:TOK-TOK.TOK.TOK.TOK": self.parse_fmt8,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt9,
            "TOK:TOK-TOK.TOK.TOK": self.parse_fmt10,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [CAT, TGT, FAM, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF]

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, CAT, TGT, FAM]

    # TOK-TOK-TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE, CAT, TGT, FAM, SUF]

    # TOK-TOK-TOK:TOK:TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, PRE, PRE, CAT, TGT, FAM, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [PRE, CAT, TGT, FAM, SUF]

    # TOK-TOK-TOK:TOK:TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        return [PRE, PRE, PRE, PRE, CAT, TGT, FAM]

    # TOK:TOK-TOK.TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        return [PRE, CAT, CAT, TGT, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt9(self, tokens):
        if tokens[3].isnumeric():
            if len(tokens[2]) <= 2 and tokens[2] != "VB":
                fmt = [CAT, PRE, SUF, SUF, SUF]
            else:
                fmt = [CAT, PRE, FAM, SUF, SUF]
        elif tokens[3].islower() and not any([c.isdigit() for c in tokens[3]]):
            fmt = [CAT, TGT, FAM, SUF, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            if tokens[2].isupper():
                fmt = [CAT, TGT, UNK, SUF, SUF] # Bad format
            else:
                fmt = [CAT, TGT, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, UNK, UNK, SUF] # Bad format
        return fmt

    # TOK:TOK-TOK.TOK.TOK
    def parse_fmt10(self, tokens):
        if tokens[4] == "Generic":
            fmt = [PRE, CAT, CAT, TGT, PRE]
        else:
            fmt = [PRE, CAT, CAT, UNK, UNK] # Bad format
        return fmt

