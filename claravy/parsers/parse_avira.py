import re
from claravy.taxonomy import *


class Parse_Avira: # Renamed from Antivir. Format somewhat similar to TheHacker, but probably not related. Partnership with F-Secure.

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK/TOK": self.parse_delim_fmt4,
            "TOK.TOK": self.parse_delim_fmt5,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric() or re.match(r"^Gen[0-9]*$", tokens[2]):
            tax = [PRE, FAM, SUF]
        else: # Bad format
            tax = [PRE, UNK, UNK]
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [CAT, UNK, UNK, SUF]
        if tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            tax = [CAT, FAM, SUF, SUF]
        elif tokens[2].isupper() and len(tokens[2]) <= 4:
            tax = [CAT, FAM, SUF, SUF]
        else:
            tax = [CAT, CAT, FAM, SUF]
        return tax

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif not tokens[3].isupper() and not tokens[3].islower() and not tokens[3].isnumeric():
            if tokens[4] == "Gen":
                tax = [PRE, PRE, PRE, PRE, SUF]
            elif tokens[2].isnumeric() or tokens[2].islower() or len(tokens[2]) <= 2:
                tax = [PRE, FAM, SUF, SUF, SUF]
            else: # Bad format
                tax = [PRE, UNK, UNK, UNK, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower():
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[2].isupper() and len(tokens[2]) == 3: # Bad format
            tax = [PRE, UNK, UNK, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK/TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric():
            tax = [PRE, SUF]
        elif tokens[1].islower() or tokens[1].isupper(): # Bad format
            tax = [UNK, UNK]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [UNK, UNK]
        if tokens[0].islower() or tokens[1].islower(): # Bad format
            tax = [UNK, UNK]
        elif tokens[1].isnumeric() or len(tokens[1]) == 1 or tokens[1].isupper():
            tax = [FAM, SUF]
        else: # Bad format
            tax = [UNK, UNK]
        return tax
