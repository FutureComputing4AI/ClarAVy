import re
from claravy.taxonomy import *


class Parse_Ahnlabv3:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK": self.parse_delim_fmt3,
            "TOK-TOK/TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK/TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK-TOK/TOK": self.parse_delim_fmt6,
            "TOK/TOK.TOK_TOK.TOK": self.parse_delim_fmt7,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK.TOK": self.parse_delim_fmt9,
            "TOK-TOK.TOK": self.parse_delim_fmt10,
            "TOK/TOK-TOK-TOK": self.parse_delim_fmt11,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[2].isupper() and len(tokens[2]) <= 3 and tokens[2] not in ["VB", "BHO", "WOW"]:
            tax = [PRE, FAM, SUF]
        elif tokens[2].isnumeric() or re.match(r"^Gen[0-9]*$", tokens[2]):
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].islower() or len(tokens[2]) == 1 or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, FAM]

    # TOK-TOK/TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [FILE, PRE, FAM, SUF]

    # TOK-TOK/TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, CAT, FAM, SUF, SUF]

    # TOK-TOK/TOK
    def parse_delim_fmt6(self, tokens):
        return [FILE, CAT, FAM]

    # TOK/TOK.TOK_TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, FILE, PRE, FAM, SUF]

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [FILE, UNK, UNK, SUF, SUF]
        if tokens[3].isnumeric():
            tax = [FILE, FAM, CAT, SUF, SUF]
        elif len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt9(self, tokens):
        # TODO: Inconsistent format
        return [UNK, UNK]

    # TOK-TOK.TOK
    def parse_delim_fmt10(self, tokens):
        return [FAM, FAM, SUF]

    #TOK/TOK-TOK-TOK
    def parse_delim_fmt11(self, tokens):
        return [PRE, VULN, VULN, VULN]
