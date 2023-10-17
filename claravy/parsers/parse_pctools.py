from claravy.taxonomy import *


class Parse_Pctools:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK": self.parse_fmt1,
            "TOK.TOK!TOK": self.parse_fmt2,
            "TOK-TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
            "TOK-TOK.TOK!TOK": self.parse_fmt5,
        }

    # TOK.TOK
    def parse_fmt1(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) <= 2 or tokens[1].lower() == "gen":
            if tokens[0].isupper():
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif tokens[1].isupper():
                fmt = [PRE, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK!TOK
    def parse_fmt2(self, tokens):
        return [CAT, FAM, SUF]

    # TOK-TOK.TOK
    def parse_fmt3(self, tokens):
        if tokens[2].isnumeric():
            fmt = [UNK, UNK, SUF] # Bad format
        else:
            fmt = [CAT, CAT, FAM]
        return fmt

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[0].isupper() or len(tokens[0]) <= 3:
                fmt = [UNK, SUF, SUF]
            else:
                fmt = [FAM, SUF, SUF]
        elif tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric() or tokens[2].lower() == "gen":
            if len(tokens[1]) <= 2 and tokens[1] != "VB":
                if tokens[0].isupper():
                    fmt = [UNK, UNK, SUF] # Bad format
                else:
                    fmt = [FAM, SUF, SUF]
            elif tokens[1].isupper() and tokens[1] != "VB":
                fmt = [PRE, UNK, SUF] # Bad format
            else:
                fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, UNK, UNK] # Bad format
        return fmt

    # TOK-TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        return [CAT, CAT, FAM, SUF]
