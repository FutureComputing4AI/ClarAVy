from claravy.taxonomy import *


class Parse_Esafe:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK TOK/TOK": self.parse_delim_fmt5,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 or tokens[2].isnumeric() or tokens[2].lower() == "gen":
            tax = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            tax = [PRE, UNK, UNK] # Bad format
        elif tokens[2].islower():
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, UNK, UNK] # Bad format
        return tax

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].islower() or tokens[1].lower() == "gen":
            if tokens[0].isupper() or len(tokens[0]) <= 2:
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        else:
            tax = [FILE, FAM]
        return tax

    # TOK TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, UNK]
        if tokens[0].lower() == "suspicious":
            tax = [PRE, PRE]
        elif tokens[1].isnumeric() or len(tokens[1]) <= 2 or tokens[1].isupper() or tokens[1].startswith("v"):
            tax = [FAM, SUF]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[1].isnumeric() or tokens[1].islower():
            tax = [FAM, SUF, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower():
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper() or len(tokens[2]) <= 3:
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK TOK/TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, PRE]
