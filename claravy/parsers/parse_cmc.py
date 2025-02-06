import re
from claravy.taxonomy import *


class Parse_Cmc:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK-TOK.TOK.TOK!TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt3,
            "TOK-TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt4,
            "TOK-TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK.TOK!TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK-TOK.TOK!TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt8
        }

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, FILE, UNK, SUF]
        if re.match(r"^[a-f0-9]{10}$", tokens[2]):
            tax = [CAT, FILE, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF]
        return tax

    # TOK-TOK.TOK.TOK!TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK.TOK.TOK.TOK!TOK"
    def parse_delim_fmt3(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF, SUF]

    # TOK-TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        return [CAT, CAT, FILE, SUF]

    # TOK.TOK!TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, FILE, SUF]

    # TOK.TOK.TOK-TOK.TOK!TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, FILE, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt8(self, tokens):
        tax = [UNK, UNK, UNK, UNK, UNK, UNK]
        if tokens[3].isnumeric():
            tax = [CAT, FILE, FAM, SUF, SUF, SUF]
        return tax
