import re
from claravy.taxonomy import *


class Parse_Ikarus:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK-TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK-TOK:TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK-TOK-TOK:TOK.TOK.TOK": self.parse_delim_fmt7,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK-TOK": self.parse_delim_fmt9,
            "TOK": self.parse_delim_fmt10,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[0] == "Packer":
            if len(tokens[2]) == 1:
                tax = [PRE, PACK, SUF]
            else:
                tax = [PRE, PRE, PACK]
        if tokens[2].isnumeric() or re.match(r"^Gen[0-9]+$", tokens[2]):
            tax = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            tax = [PRE, UNK, UNK] # Bad format
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) == 1:
            tax = [FAM, SUF]
        elif re.match(r"^CVE[0-9]+$", tokens[1]):
            tax = [PRE, VULN]
        else:
            tax = [PRE, FAM]
        return tax # Kind of messy format, but parsed ok

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, UNK, UNK, UNK]
        if tokens[3].isupper():
            tax = [PRE, PRE, UNK, UNK]
        elif tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF]
        else:
            tax = [CAT, CAT, FILE, FAM]
        return tax

    # TOK-TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [CAT, CAT, UNK]
        if tokens[2].isupper():
            tax = [CAT, CAT, UNK]
        elif tokens[2].isnumeric() or re.match(r"^Gen[0-9]+$", tokens[2]):
            tax = [CAT, CAT, SUF]
        else:
            tax = [CAT, CAT, FAM]
        return tax

    # TOK-TOK-TOK:TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, PRE, PRE, FAM] # Also kind of messy but parsed ok

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [UNK, UNK, UNK, UNK]
        if tokens[1].isnumeric():
            tax = [FAM, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3].islower():
            if (tokens[2].isupper() or len(tokens[2]) <= 2) and tokens[2] != "VB":
                tax = [PRE, UNK, UNK, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 and tokens[2] != "VB":
            tax = [PRE, PRE, FAM, SUF]
        elif tokens[3].isupper():
            tax = [PRE, PRE, UNK, UNK] # Bad format
        elif tokens[3] == "Based":
            tax = [PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM]
        return tax

    # TOK-TOK-TOK:TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [PRE, PRE, PRE] + self.parse_delim_fmt1(tokens[3:])

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [UNK, UNK, UNK, UNK, SUF]
        if tokens[3].isupper() and tokens[3] != "VB":
            tax = [PRE, PRE, UNK, UNK, SUF]
        elif tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [CAT, CAT, FILE, FAM, SUF]
        return tax

    # TOK-TOK
    def parse_delim_fmt9(self, tokens):
        if tokens[1].isnumeric():
            tax = [FAM, SUF]
        elif tokens[0] in ["Tojan", "Trojan"]:
            tax = [CAT, CAT]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK
    def parse_delim_fmt10(self, tokens):
        return [FAM]
