from claravy.taxonomy import *


class Parse_Zoner:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        if tokens[2].isnumeric():
            fmt = [CAT, TGT, SUF]
        elif tokens[2].isupper() and tokens[1] != "VB":
            if tokens[1].isupper():
                fmt = [CAT, TGT, SUF]
            else:
                fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, UNK, UNK] # Bad format
        return fmt

    # TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, FAM]

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [CAT, UNK, UNK, SUF]
        if tokens[3].isnumeric():
            fmt = [CAT, TGT, FAM, SUF]
        else:
            fmt = [CAT, UNK, UNK, SUF] # Bad format
        return fmt
