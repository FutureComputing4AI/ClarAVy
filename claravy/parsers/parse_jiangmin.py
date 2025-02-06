import re
from claravy.taxonomy import *


class Parse_Jiangmin:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK/TOK.TOK": self.parse_delim_fmt5,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK, UNK]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            tax = [PRE, VULN, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif tokens[2].islower() or tokens[2].isnumeric() or tokens[2].startswith("Gen"):
            tax = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            tax = [PRE, UNK, UNK]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].islower() or tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[1].isnumeric():
            tax = [FAM, SUF, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower() or tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK-TOK/TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [CAT, CAT, UNK, UNK]
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            tax = [CAT, CAT, FAM, SUF]
        elif tokens[2].isupper():
            tax = [CAT, CAT, PRE, FAM]
        else:
            tax = [CAT, CAT, UNK, UNK] # Bad format
        return tax
