import re
from claravy.taxonomy import *


class Parse_Maxsecure:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK-TOK-TOK:TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK-TOK-TOK-TOK.TOK": self.parse_delim_fmt5,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            tax = [PRE, PRE, SUF, SUF]
        elif tokens[2] == "Heur":
            tax = [PRE, UNK, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        if tokens[2].islower() or tokens[2].isupper() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            tax = [PRE, FAM, SUF]
        elif re.match(r"^.*Gen[0-9]*$", tokens[2]) or tokens[2] == "Dam":
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[:3] == ["Not", "a", "virus"]:
            tax = [PRE, PRE, PRE, PRE, FAM]
        elif tokens[3].isnumeric():
            tax = [CAT, FILE, FAM, SUF, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            tax = [CAT, PRE, FAM, SUF, SUF]
        else:
            tax = [CAT, PRE, FILE, FAM, SUF]
        return tax

    # TOK-TOK-TOK:TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE, CAT, FAM, SUF]

    # TOK-TOK-TOK-TOK-TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, PRE, CAT, FAM, SUF]
