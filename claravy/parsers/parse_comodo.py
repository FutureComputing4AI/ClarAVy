from claravy.taxonomy import *


class Parse_Comodo:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK@TOK": self.parse_fmt2,
            "TOK": self.parse_fmt3,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK@#TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK@TOK": self.parse_fmt6,
            "TOK.TOK.TOK.~TOK": self.parse_fmt7,
            "TOK.TOK.TOK.TOK.~TOK": self.parse_fmt8,
            "TOK.TOK.TOK": self.parse_fmt9,
            "TOK.TOK.TOK.TOK.~TOK@TOK": self.parse_fmt10,
            "TOK.TOK.TOK.~TOK@TOK": self.parse_fmt11,
            "TOK.TOK": self.parse_fmt12,
            "TOK.TOK!": self.parse_fmt13,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, TGT, UNK, SUF]
        if tokens[0] == "Packed":
            fmt = [PRE, TGT, PACK, SUF]
        else:
            fmt = [PRE, TGT, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK@TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, TGT, UNK, SUF, SUF]

        if tokens[0] == "Packed":
            fmt = [PRE, TGT, PACK, SUF, SUF]
        else:
            fmt = [PRE, TGT, FAM, SUF, SUF]
        return fmt

    # TOK
    def parse_fmt3(self, tokens):
        return [PRE]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, TGT, CAT, FAM, SUF]

    # TOK@#TOK
    def parse_fmt5(self, tokens):
        return [PRE, SUF]

    # TOK.TOK.TOK.TOK.TOK@TOK
    def parse_fmt6(self, tokens):
        return [PRE, TGT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.~TOK
    def parse_fmt7(self, tokens):
        return [CAT, TGT, FAM, SUF]

    # TOK.TOK.TOK.TOK.~TOK
    def parse_fmt8(self, tokens):
        return [PRE, TGT, CAT, FAM, SUF]

    # TOK.TOK.TOK
    def parse_fmt9(self, tokens):
        if tokens[1] == "Pck":
            fmt = [PRE, PRE, PACK]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK.~TOK@TOK
    def parse_fmt10(self, tokens):
        return [PRE, TGT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.~TOK@TOK
    def parse_fmt11(self, tokens):
        return [CAT, TGT, FAM, SUF, SUF]

    # TOK.TOK
    def parse_fmt12(self, tokens):
        if tokens[0] == "Heur":
            fmt = [PRE, PRE]
        elif len(tokens[1]) <= 2 or tokens[1].isnumeric() or tokens[1].isupper() or tokens[1].islower():
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK!
    def parse_fmt13(self, tokens):
        return self.parse_fmt12(tokens) + [NULL]

