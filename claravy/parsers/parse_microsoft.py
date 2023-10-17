import re
from claravy.taxonomy import *


class Parse_Microsoft:

    def __init__(self):
        self.parse_fmt = {
            "TOK:TOK/TOK.TOK": self.parse_fmt1,
            "TOK:TOK/TOK": self.parse_fmt2,
            "TOK:TOK/TOK.TOK!TOK": self.parse_fmt3,
            "TOK:TOK/TOK!TOK": self.parse_fmt4,
            "TOK:TOK/TOK.TOK@TOK": self.parse_fmt5,
        }

    # TOK:TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [CAT, TGT, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF]
        return fmt

    # TOK:TOK/TOK
    def parse_fmt2(self, tokens):
        fmt = [CAT, TGT, UNK]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN]
        else:
            fmt = [CAT, TGT, FAM]
        return fmt

    # TOK:TOK/TOK.TOK!TOK
    def parse_fmt3(self, tokens):
        fmt = [CAT, TGT, UNK, SUF, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF, SUF]
        return fmt

    # TOK:TOK/TOK!TOK
    def parse_fmt4(self, tokens):
        fmt = [CAT, TGT, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF]
        return fmt

    # TOK:TOK/TOK.TOK@TOK
    def parse_fmt5(self, tokens):
        fmt = [CAT, TGT, UNK, SUF, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF, SUF]
        return fmt
