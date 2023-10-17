from claravy.taxonomy import *


class Parse_Cyren: # Renamed from Commtouch to Cyren, Acquired F-prot

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK!TOK": self.parse_fmt2,
            "TOK/TOK.TOK!TOK": self.parse_fmt3,
            "TOK/TOK-TOK!TOK": self.parse_fmt4,
            "TOK/TOK.TOK-TOK": self.parse_fmt5,
            "TOK/TOK.TOK.TOK": self.parse_fmt6,
            "TOK/TOK": self.parse_fmt7,
            "TOK/TOK_TOK.TOK.TOK!TOK": self.parse_fmt8,
            "TOK.TOK": self.parse_fmt9,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        return [TGT, FAM, SUF]

    # TOK/TOK.TOK.TOK!TOK"
    def parse_fmt2(self, tokens):
        return [TGT, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK!TOK
    def parse_fmt3(self, tokens):
        if tokens[3] == "Olympus":
            fmt = [TGT, PRE, SUF, SUF]
        else:
            fmt = [TGT, FAM, SUF, SUF]
        return fmt

    # TOK/TOK-TOK!TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            fmt = [PRE, SUF, SUF, SUF]
        elif tokens[1] == "Heuristic":
            if tokens[2].isupper() or tokens[2].isnumeric():
                fmt = [PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        elif tokens[2] == "based":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].islower() or tokens[2].isupper():
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK-TOK
    def parse_fmt5(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK/TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK/TOK
    def parse_fmt7(self, tokens):
        return [TGT, FAM]

    # TOK/TOK_TOK.TOK.TOK!TOK
    def parse_fmt8(self, tokens):
        return [TGT, UNK, UNK, SUF, SUF, SUF] # Bad format

    # TOK.TOK
    def parse_fmt9(self, tokens):
        if tokens[1] == "gen":
            fmt = [PRE, SUF]
        elif tokens[1].isnumeric() or len(tokens[1]) <= 2:
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt
