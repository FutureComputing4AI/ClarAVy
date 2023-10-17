from claravy.taxonomy import *


class Parse_Drweb:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK": self.parse_fmt3,
            "TOK TOK TOK.TOK.TOK": self.parse_fmt4,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[2] == "Packed":
            fmt = [PRE, PACK, PRE]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF]
        elif tokens[2].lower() in ["based", "origin"]:
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].lower() == "based":
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[0].isupper() or len(tokens[0]) <= 2:
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif tokens[1].islower():
            fmt = [FAM, SUF]
        else:
            fmt = [UNK, UNK] # Usually [PRE, FAM] but rarely are families in tokens[0] and tokens[1]
        return fmt

    # TOK TOK TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]
