from claravy.taxonomy import *


class Parse_Nprotect: # Renamed to Tachyon

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK/TOK.TOK.TOK": self.parse_fmt4,
            "TOK:TOK.TOK.TOK": self.parse_fmt5,
            "TOK-TOK/TOK.TOK.TOK": self.parse_fmt6,
            "TOK-TOK/TOK.TOK.TOK.TOK": self.parse_fmt7,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt8,
            "TOK/TOK.TOK": self.parse_fmt9,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            fmt = [PRE, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [CAT, TGT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            if len(tokens[1]) == 1:
                fmt = [FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic":
            fmt = [PRE, PRE, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [CAT, TGT, FAM, SUF]

    # TOK:TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK-TOK/TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF]

    # TOK-TOK/TOK.TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if len(tokens[3]) <= 2 and tokens[3].upper() != "VB":
            fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[3].isupper() and tokens[3] != "VB":
            fmt = [PRE, PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK
    def parse_fmt9(self, tokens):
        return [CAT, TGT, FAM]


