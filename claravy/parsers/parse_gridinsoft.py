from claravy.taxonomy import *


class Parse_Gridinsoft:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK!TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK!.TOK": self.parse_fmt3,
            "TOK.TOK.TOK!TOK": self.parse_fmt4,
            "TOK.TOK.TOK.TOK!TOK-TOK": self.parse_fmt5,
            "TOK.TOK_TOK.TOK!TOK": self.parse_fmt6,
        }

    # TOK.TOK.TOK.TOK!TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, UNK, UNK, UNK]
        if len(tokens[2]) == 1:
            fmt = [CAT, FAM, SUF, SUF, SUF]
        elif tokens[1].startswith("Win"):
            fmt = [CAT, TGT, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK.TOK!TOK
    def parse_fmt2(self, tokens):
        fmt = [CAT, TGT, FAM, SUF, SUF]
        if len(tokens[1]) == 1:
            fmt = [CAT, SUF, FAM, SUF, SUF]
        return fmt

    # TOK.TOK!.TOK
    def parse_fmt3(self, tokens):
        return [PRE, SUF, SUF]

    # TOK.TOK.TOK!TOK
    def parse_fmt4(self, tokens):
        return [CAT, FAM, SUF, SUF]

    #TOK.TOK.TOK.TOK!TOK-TOK
    def parse_fmt5(self, tokens):
        return self.parse_fmt2(tokens) + [SUF]

    # TOK.TOK_TOK.TOK!TOK
    def parse_fmt6(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]
