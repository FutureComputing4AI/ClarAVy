from claravy.taxonomy import *


class Parse_Esafe:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK TOK": self.parse_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK TOK/TOK": self.parse_fmt5,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        if tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 or tokens[2].isnumeric() or tokens[2].lower() == "gen":
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, UNK, UNK] # Bad format
        elif tokens[2].islower():
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, UNK, UNK] # Bad format
        return fmt

    # TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].islower() or tokens[1].lower() == "gen":
            if tokens[0].isupper() or len(tokens[0]) <= 2:
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        else:
            fmt = [TGT, FAM]
        return fmt

    # TOK TOK
    def parse_fmt3(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0].lower() == "suspicious":
            fmt = [PRE, PRE]
        elif tokens[1].isnumeric() or len(tokens[1]) <= 2 or tokens[1].isupper() or tokens[1].startswith("v"):
            fmt = [FAM, SUF]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[1].isnumeric() or tokens[1].islower():
            fmt = [FAM, SUF, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower():
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper() or len(tokens[2]) <= 3:
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK TOK/TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, PRE]
