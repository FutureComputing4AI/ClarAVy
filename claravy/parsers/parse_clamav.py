from claravy.taxonomy import *


class Parse_Clamav:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK-TOK": self.parse_fmt1,
            "TOK.TOK-TOK": self.parse_fmt2,
            "TOK.TOK.TOK-TOK-TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK-TOK-TOK-TOK": self.parse_fmt5,
            "TOK.TOK": self.parse_fmt6,
            "TOK.TOK.TOK.TOK": self.parse_fmt7,
        }

    # TOK.TOK.TOK-TOK
    def parse_fmt1(self, tokens):
        if tokens[1] == "Packed":
            fmt = [PRE, PRE, PACK, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, CAT, FAM, SUF]
        return fmt

    # TOK.TOK-TOK
    def parse_fmt2(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK-TOK-TOK
    def parse_fmt3(self, tokens):
        return [TGT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        if tokens[1] == "Packed":
            fmt = [PRE, PRE, PACK]
        elif tokens[2].isnumeric():
            if tokens[1].isnumeric():
                if tokens[0].isupper():
                    fmt = [SUF, SUF, SUF]
                else:
                    fmt = [FAM, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2:
            if tokens[1].isnumeric():
                fmt = [FAM, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF]
        elif tokens[2].lower() == "gen":
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isupper(): # Bad format
            fmt = [PRE, UNK, UNK]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK-TOK-TOK-TOK
    def parse_fmt5(self, tokens):
        return [TGT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].islower():
            if len(tokens[0]) <= 2 and tokens[0] != "VB":
                fmt = [SUF, SUF]
            else:
                fmt = [FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        if tokens[1] == "Packed":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[3].isupper() or tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            fmt = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            fmt = [PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM]
        return fmt

