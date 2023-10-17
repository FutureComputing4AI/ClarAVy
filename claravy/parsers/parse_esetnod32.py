from claravy.taxonomy import *


class Parse_Esetnod32: # Renamed from nod32

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK TOK TOK TOK/TOK.TOK": self.parse_fmt2,
            "TOK/TOK.TOK.TOK": self.parse_fmt3,
            "TOK TOK TOK TOK/TOK.TOK.TOK": self.parse_fmt4,
            "TOK TOK TOK TOK/TOK.TOK TOK TOK": self.parse_fmt5,
            "TOK/TOK.TOK TOK TOK": self.parse_fmt6,
            "TOK TOK TOK TOK/TOK.TOK.TOK TOK TOK": self.parse_fmt7,
            "TOK/TOK": self.parse_fmt8,
            "TOK TOK TOK TOK/TOK": self.parse_fmt9,
            "TOK TOK TOK TOK TOK/TOK.TOK": self.parse_fmt10,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        return [TGT, FAM, SUF]

    # TOK TOK TOK TOK/TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE, PRE, TGT, FAM, SUF]

    # TOK/TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [TGT, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            fmt = [TGT, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [TGT, FAM, SUF, SUF]
        elif tokens[2].isupper() and len(tokens[2]) == 3:
            fmt = [TGT, UNK, UNK, SUF] # Bad format
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK TOK TOK TOK/TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE] + self.parse_fmt3(tokens[3:])

    # TOK TOK TOK TOK/TOK.TOK TOK TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, PRE, TGT, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK TOK TOK
    def parse_fmt6(self, tokens):
        return [TGT, FAM, SUF, SUF, SUF]

    # TOK TOK TOK TOK/TOK.TOK.TOK TOK TOK
    def parse_fmt7(self, tokens):
        fmt = [PRE, PRE, PRE, TGT, UNK, UNK, SUF, SUF, SUF]
        if tokens[5].isupper():
            fmt = [PRE, PRE, PRE, TGT, FAM, SUF, SUF, SUF, SUF]
        elif tokens[4] == "FlyStudio":
            fmt = [PRE, PRE, PRE, TGT, FAM, SUF, SUF, SUF, SUF] # Bad format - only for FlyStudio
        else:
            fmt = [PRE, PRE, PRE, TGT, CAT, FAM, SUF, SUF, SUF]
        return fmt

    # TOK/TOK
    def parse_fmt8(self, tokens):
        return [TGT, FAM]

    # TOK TOK TOK TOK/TOK
    def parse_fmt9(self, tokens):
        return [PRE, PRE, PRE, TGT, FAM]

    # TOK TOK TOK TOK TOK/TOK.TOK
    def parse_fmt10(self, tokens):
        return [PRE, PRE, PRE, PRE, TGT, FAM, SUF]
