import re
from claravy.taxonomy import *


class Parse_Cmc:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK!TOK": self.parse_fmt1,
            "TOK-TOK.TOK.TOK!TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK!TOK": self.parse_fmt3,
            "TOK-TOK.TOK.TOK.TOK!TOK": self.parse_fmt4,
            "TOK-TOK.TOK!TOK": self.parse_fmt5,
            "TOK.TOK!TOK": self.parse_fmt6,
            "TOK.TOK.TOK-TOK.TOK!TOK": self.parse_fmt7,
            "TOK.TOK.TOK.TOK.TOK!TOK": self.parse_fmt8
        }

    # TOK.TOK.TOK!TOK
    def parse_fmt1(self, tokens):
        fmt = [CAT, TGT, UNK, SUF]
        if re.match(r"^[a-f0-9]{10}$", tokens[2]):
            fmt = [CAT, TGT, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF]
        return fmt

    # TOK-TOK.TOK.TOK!TOK
    def parse_fmt2(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF]

    # TOK.TOK.TOK.TOK!TOK"
    def parse_fmt3(self, tokens):
        return [CAT, TGT, FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK!TOK
    def parse_fmt4(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, SUF]

    # TOK-TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        return [CAT, CAT, TGT, SUF]

    # TOK.TOK!TOK
    def parse_fmt6(self, tokens):
        return [CAT, TGT, SUF]

    # TOK.TOK.TOK-TOK.TOK!TOK
    def parse_fmt7(self, tokens):
        return [CAT, TGT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK!TOK
    def parse_fmt8(self, tokens):
        fmt = [UNK, UNK, UNK, UNK, UNK, UNK, UNK]
        if tokens[3].isnumeric():
            fmt = [CAT, TGT, FAM, SUF, SUF, SUF]
        return fmt
