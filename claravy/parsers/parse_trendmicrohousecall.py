import re
from claravy.taxonomy import *


class Parse_Trendmicrohousecall: # Same company as Trendmicro

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK_TOK.TOK": self.parse_delim_fmt1,
            "TOK_TOK_TOK.TOK": self.parse_delim_fmt2,
            "TOK_TOK.TOK-TOK": self.parse_delim_fmt3,
            "TOK_TOK": self.parse_delim_fmt4,
            "TOK_TOK-TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
        }

    # TOK_TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, SUF]
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [PRE, SUF, SUF]
        elif len(tokens[1]) == 3:
            tax = [UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK_TOK_TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, SUF, SUF]
        if len(tokens[1]) <= 3:
            tax = [PRE, UNK, SUF, SUF] # Bad format
        else:
            tax = [PRE, FAM, SUF, SUF]
        return tax

    # TOK_TOK.TOK-TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, FAM, SUF, SUF]

    # TOK_TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].islower():
            tax = [UNK, SUF] # Bad format
        elif len(tokens[1]) <= 3:
            tax = [PRE, UNK] # Bad format
        else:
            tax = [PRE, FAM]
        return tax

    # TOK_TOK-TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, UNK, SUF]
        if re.match(r"CVE[0-9]+", tokens[1]):
            tax = [PRE, VULN, SUF]
        elif len(tokens[1]) <= 4:
            tax = [PRE, UNK, SUF] # Bad format
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, FILE, FAM, SUF]
