from claravy.taxonomy import *


class Parse_Vba32:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK-TOK.TOK.TOK": self.parse_fmt4,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK-TOK.TOK.TOK": self.parse_fmt6,
            "TOK.TOK-TOK.TOK": self.parse_fmt7,
            "TOK-TOK.TOK": self.parse_fmt8,
            "TOK TOK TOK.TOK.TOK.TOK": self.parse_fmt9,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[2].isnumeric():
            if len(tokens[1]) <= 2 and tokens[1] != "VB":
                fmt = [PRE, SUF, SUF]
            elif len(tokens[1]) == 3 and tokens[1].isupper():
                fmt = [PRE, UNK, SUF] # Bad format
            else:
                fmt = [PRE, FAM, SUF]
        elif tokens[2].islower():
            fmt = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            fmt = [PRE, UNK, UNK] # Bad format
        elif tokens[2] == "Heur":
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[0].isupper() or len(tokens[0]) <= 3:
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif tokens[1].islower():
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3].isupper() or len(tokens[3]) <= 2:
            if tokens[2].isupper() and tokens[2] != "VB":
                fmt = [PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 4 and tokens[3].endswith("en"): # Gen, Sen, cGen
            if tokens[2].isupper() and tokens[2] != "VB":
                fmt = [PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        elif tokens[3] == "Heur":
            fmt = [PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM]
        return fmt

    # TOK.TOK-TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        if tokens[4].isnumeric() or tokens[4].isupper() or tokens[4].islower():
            if tokens[3].isupper():
                fmt = [PRE, PRE, PRE, UNK, SUF] # Bad format
            else:
                fmt = [PRE, CAT, CAT, FAM, SUF]
        elif len(tokens[4]) <= 3 or tokens[3] != "Win32":
            fmt = [PRE, PRE, PRE, UNK, UNK] # Bad format
        else:
            fmt = [PRE, CAT, CAT, TGT, FAM] # Only Win32 left
        return fmt

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [CAT, CAT, UNK, UNK, SUF]
        if tokens[3] == "gen":
            fmt = [CAT, CAT, FAM, SUF, SUF]
        else:
            fmt = [CAT, CAT, TGT, FAM, SUF]
        return fmt

    # TOK-TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [CAT, CAT, UNK, UNK]
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "gen":
            if tokens[2].isupper() and len(tokens[2]) <= 3 and tokens[2] != "VB":
                fmt = [CAT, CAT, UNK, UNK] # Bad format
            else:
                fmt = [CAT, CAT, FAM, SUF]
        elif len(tokens[3]) <= 3:
            fmt = [CAT, CAT, UNK, UNK] # Bad format
        else:
            fmt = [CAT, CAT, PRE, FAM]
        return fmt

    # TOK.TOK-TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [PRE, CAT, CAT, UNK]
        if tokens[3].isnumeric() or tokens[3].islower():
            fmt = [PRE, CAT, CAT, SUF]
        elif tokens[3].isupper():
            fmt = [PRE, CAT, CAT, UNK] # Bad format
        else:
            fmt = [PRE, CAT, CAT, FAM]
        return fmt

    # TOK-TOK.TOK
    def parse_fmt8(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[1] == "based":
            fmt = [PRE, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower():
            fmt = [PRE, CAT, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, CAT, UNK] # Bad format
        else:
            fmt = [PRE, CAT, FAM]
        return fmt

    # TOK TOK TOK.TOK.TOK.TOK
    def parse_fmt9(self, tokens):
        fmt = [PRE, PRE, PRE, PRE, UNK, UNK]
        if tokens[5].isnumeric() or tokens[5].isupper() or tokens[5].islower():
            fmt = [PRE, PRE, PRE, PRE, FAM, UNK]
        elif len(tokens[5]) <= 2 and tokens[5] != "VB":
            fmt = [PRE, PRE, PRE, PRE, FAM, UNK]
        else:
            fmt = [PRE, PRE, PRE, PRE, PRE, FAM]
        return fmt
