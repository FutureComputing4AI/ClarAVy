from claravy.taxonomy import *


class Parse_Symantec:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK.TOK!TOK": self.parse_fmt3,
            "TOK": self.parse_fmt4,
            "TOK TOK": self.parse_fmt5,
            "TOK.TOK.TOK!TOK": self.parse_fmt6,
            "TOK.TOK.TOK.TOK": self.parse_fmt7,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif tokens[2].isnumeric() or len(tokens[2]) <= 2 or tokens[2].isupper():
            if tokens[1].isupper():
                fmt = [UNK, UNK, SUF] # Bad format
            else:
                fmt = [PRE, FAM, SUF]
        else:
            fmt = [UNK, UNK, UNK] # Bad format - may be able to parse more?
        return fmt

    # TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].isupper() or tokens[1].islower():
            if tokens[0].isupper():
                fmt = [UNK, UNK] # Bad format
            else:
                fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK!TOK
    def parse_fmt3(self, tokens):
        return [PRE, FAM, SUF]

    # TOK
    def parse_fmt4(self, tokens):
        return [FAM]

    # TOK TOK
    def parse_fmt5(self, tokens):
        # Either [CAT, CAT] or [FAM, FAM]
        return [UNK, UNK] # Bad format

    # TOK.TOK.TOK!TOK
    def parse_fmt6(self, tokens):
        return self.parse_fmt1(tokens) + [SUF]

    # TOK.TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [UNK, UNK, UNK, UNK]
        if tokens[1].isnumeric():
            fmt = [UNK, SUF, UNK, SUF] # Bad format
        elif tokens[0] == "Suspicious":
            fmt = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric():
            if tokens[1].islower():
                fmt = [UNK, SUF, SUF, SUF] # Bad format
            else:
                fmt = [PRE, FAM, SUF, SUF] # Some of PRE are family-like? Unsure
        elif len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, UNK] # Last token either CAT or SUF
        elif tokens[0] == "Heur":
            fmt = [PRE, PRE, SUF, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt
