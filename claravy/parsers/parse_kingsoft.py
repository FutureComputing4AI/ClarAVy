from claravy.taxonomy import *


class Parse_Kingsoft:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK.(TOK)": self.parse_fmt1,
            "TOK.TOK.TOK.(TOK)": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK_TOK.TOK.(TOK)": self.parse_fmt4,
            "TOK_TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt6,
        }

    # TOK.TOK.TOK.TOK.(TOK)
    def parse_fmt1(self, tokens):
        fmt = [PRE, PRE, UNK, SUF, SUF, NULL]
        if tokens[2].isnumeric():
            fmt = [PRE, PRE, SUF, SUF, SUF, NULL]
        elif tokens[1].startswith("Heur"):
            fmt = [PRE, PRE, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.(TOK)
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF, NULL]
        if len(tokens[2]) == 1 or tokens[2].islower():
            fmt = [PRE, FAM, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, FAM, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if len(tokens[2]) == 1 or tokens[2].islower():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK_TOK.TOK.(TOK)
    def parse_fmt4(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[2] == "Heur" and tokens[3] == "Generic":
            fmt = [PRE, PRE, PRE, PRE, SUF, SUF, NULL]
        elif tokens[3].isnumeric() or len(tokens[3]) <= 2:
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        elif tokens[3].islower():
            fmt = [PRE, PRE, SUF, FAM, SUF, SUF, NULL]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF, NULL]
        elif tokens[2].islower():
            fmt = [PRE, PRE, SUF, FAM, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        return fmt

    # TOK_TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE]                                                                        

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [PRE, CAT, FAM, SUF, SUF]
