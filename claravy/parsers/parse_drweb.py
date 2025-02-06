from claravy.taxonomy import *


class Parse_Drweb:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK": self.parse_delim_fmt3,
            "TOK TOK TOK.TOK.TOK": self.parse_delim_fmt4,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[2] == "Packed":
            tax = [PRE, PACK, PRE]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF]
        elif tokens[2].lower() in ["based", "origin"]:
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].lower() == "based":
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[0].isupper() or len(tokens[0]) <= 2:
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif tokens[1].islower():
            tax = [FAM, SUF]
        else:
            tax = [UNK, UNK] # Usually [PRE, FAM] but rarely are families in tokens[0] and tokens[1]
        return tax

    # TOK TOK TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]
