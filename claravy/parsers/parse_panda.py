from claravy.taxonomy import *


class Parse_Panda:

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK TOK": self.parse_fmt2,
            "TOK/TOK": self.parse_fmt3,
            "TOK/TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK": self.parse_fmt5,
            "TOK": self.parse_fmt6,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, SUF]
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [PRE, SUF, SUF]
        elif tokens[1].isupper():
            fmt = [PRE, UNK, SUF] # Bad format
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE]

    # TOK/TOK
    def parse_fmt3(self, tokens):
        return [PRE, FAM]

    # TOK/TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt5(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) <= 2 or tokens[1].lower() == "gen":
            if tokens[0].isupper():
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif tokens[1].isupper():
            if tokens[0].isnumeric():
                fmt = [SUF, SUF]
            else:
                fmt = [FAM, SUF]
        else:
            fmt = [UNK, UNK] # Bad format
        return fmt

    # TOK
    def parse_fmt6(self, tokens):
        return [FAM]
