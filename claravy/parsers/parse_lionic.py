from claravy.taxonomy import *


class Parse_Lionic:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK!TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK!TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK.TOK.TOK!TOK": self.parse_fmt5,
        }

    # TOK.TOK.TOK.TOK!TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3].islower() or tokens[3].isnumeric() or len(tokens[3]) == 1:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK!TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 3:
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        elif tokens[2].startswith("Gen"):
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        if len(tokens[2]) == 4 and tokens[2][0].islower():
            if tokens[1].startswith("Gen"):
                fmt = [PRE, PRE, SUF]
            else:
                fmt = [PRE, FAM, SUF]
        elif tokens[2].startswith("Gen"):
            fmt = [PRE, PRE, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF, SUF]
        if tokens[4].isnumeric():
            fmt = [PRE, PRE, UNK, UNK, SUF, SUF] # Bad format
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt
