import re
from claravy.taxonomy import *


class Parse_Fortinet:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK/TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK": self.parse_delim_fmt3,
            "TOK/TOK.TOK!TOK.TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK/TOK!TOK": self.parse_delim_fmt6,
            "TOK": self.parse_delim_fmt7,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK/TOK.TOK@TOK": self.parse_delim_fmt9,
            "TOK/TOK_TOK": self.parse_delim_fmt10,
        }

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM]

    # TOK/TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, SUF]
        if re.match(r"CVE[0-9]+", tokens[2]):
            tax = [PRE, UNK, VULN]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK!TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        tax = [FILE, UNK, UNK, SUF, SUF]
        if re.match(r"CVE[0-9]+", tokens[2]):
            tax = [FILE, PRE, VULN, SUF, SUF]
        elif tokens[1] == "Generic":
            tax = [FILE, PRE, SUF, SUF, SUF]
        else:
            tax = [FILE, UNK, UNK, SUF, SUF]
        return tax

    # TOK/TOK!TOK
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, FAM, UNK]
        if tokens[2].islower() or tokens[2].isupper() or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, FAM, UNK] # Weird format - Morphine, Monder?
        return tax

    # TOK
    def parse_delim_fmt7(self, tokens):
        return [FAM]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        if tokens[2].isupper() or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt9(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK_TOK
    def parse_delim_fmt10(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[2].isnumeric() or tokens[2].islower() or tokens[2].isupper():
            if tokens[1].isupper():
                tax = [PRE, UNK, SUF] # Bad format
            else:
                tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax
