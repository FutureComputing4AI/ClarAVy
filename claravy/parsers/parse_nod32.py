from claravy.taxonomy import *


class Parse_Nod32: # Renamed to Esetnod32

    def __init__(self):
        self.parse_fmt = {
            "TOK TOK TOK TOK/TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK": self.parse_fmt2,
            "TOK/TOK.TOK.TOK": self.parse_fmt3,
            "TOK TOK TOK TOK/TOK.TOK.TOK": self.parse_fmt4,
            "TOK TOK TOK TOK TOK/TOK.TOK": self.parse_fmt5,
        }

    # TOK TOK TOK TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, PRE, PRE, TGT, FAM, SUF]

    # TOK/TOK.TOK
    def parse_fmt2(self, tokens):
        return [TGT, FAM, SUF]

    # TOK/TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        if tokens[1] == "Packed":
            fmt = [TGT, PRE, PACK, SUF]
        elif tokens[2].islower():
            fmt = [TGT, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [TGT, FAM, SUF, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            fmt = [TGT, UNK, UNK, SUF]
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK TOK TOK TOK TOK/TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE, TGT, CAT, FAM, SUF]

    # TOK TOK TOK TOK TOK/TOK.TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, PRE, PRE, TGT, FAM, SUF]

