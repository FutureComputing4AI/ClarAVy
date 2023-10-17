from claravy.taxonomy import *


class Parse_Bkav:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt5,
        }


    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [TGT, FAM, UNK] # Last token either SUF or CAT

    # TOK.TOK.
    def parse_fmt2(self, tokens):
        return [TGT, FAM, NULL]

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, UNK]
        if tokens[1].startswith("Fam"):
            if tokens[3] == "PE":
                fmt = [TGT, PRE, FAM, TGT]
            else:
                fmt = [TGT, PRE, FAM, CAT]
        elif tokens[1].startswith("Clod"):
            fmt = [PRE, SUF, UNK, UNK]
        else:
            fmt = [PRE, FAM, UNK, UNK]
        return fmt

    # TOK.TOK
    def parse_fmt4(self, tokens):
        return [UNK, FAM] # First token either SUF or TGT

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, UNK, UNK, UNK]
        if tokens[1].startswith("Fam"):
            if tokens[4] == "PE":
                fmt = [TGT, PRE, FAM, SUF, TGT]
            else:
                fmt = [TGT, PRE, FAM, SUF, CAT]
        else:
            fmt = [TGT, CAT, FAM, SUF, SUF]
        return fmt 
