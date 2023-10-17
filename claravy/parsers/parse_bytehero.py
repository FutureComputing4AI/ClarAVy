from claravy.taxonomy import *


class Parse_Bytehero:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK-TOK.TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [CAT, UNK, FAM, SUF]
        if tokens[1] == "Exception":
            fmt = [CAT, PRE, FAM, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK"
    def parse_fmt2(self, tokens):
        return [CAT, PRE, FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [CAT, CAT, PRE, FAM, SUF]
