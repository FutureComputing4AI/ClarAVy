from claravy.taxonomy import *


class Parse_Fprot: # Acquired by Commtouch/Cyren

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK.TOK!TOK": self.parse_fmt1,
            "TOK/TOK.TOK": self.parse_fmt2,
            "TOK/TOK-TOK!TOK": self.parse_fmt3,
            "TOK/TOK.TOK!TOK": self.parse_fmt4,
            "TOK/TOK.TOK.TOK": self.parse_fmt5,
            "TOK.TOK": self.parse_fmt6,
            "TOK/TOK": self.parse_fmt7,
            "TOK/TOK.TOK@TOK": self.parse_fmt8,
            "TOK/TOK_TOK.TOK.TOK!TOK": self.parse_fmt9,
        }

    # TOK/TOK.TOK.TOK!TOK
    def parse_fmt1(self, tokens):
        return [TGT, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK
    def parse_fmt2(self, tokens):
        return [TGT, FAM, SUF]

    # TOK/TOK-TOK!TOK
    def parse_fmt3(self, tokens):
        fmt = [TGT, UNK, SUF, SUF]
        if len(tokens[1]) == 1:
            fmt = [TGT, SUF, SUF, SUF]
        elif tokens[1].isupper():
            fmt = [TGT, PRE, FAM, SUF]
        else:
            fmt = [TGT, FAM, SUF, SUF]
        return fmt

    # TOK/TOK.TOK!TOK
    def parse_fmt4(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK/TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK.TOK
    def parse_fmt6(self, tokens):
        if tokens[1] == "gen":
            fmt = [PRE, SUF]
        elif tokens[1].isnumeric() or len(tokens[1]) <= 2:
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK/TOK
    def parse_fmt7(self, tokens):
        return [TGT, FAM]

    # TOK/TOK.TOK@TOK
    def parse_fmt8(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK/TOK_TOK.TOK.TOK!TOK
    def parse_fmt9(self, tokens):
        return [TGT, UNK, UNK, SUF, SUF, SUF] # Bad format
