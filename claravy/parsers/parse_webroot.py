from claravy.taxonomy import *


class Parse_Webroot:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[2].lower() == "gen" or tokens[2].islower():
            tax = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF]
        elif tokens[2].isnumeric() or tokens[2].isupper():
            tax = [PRE, UNK, SUF] # Bad format
        else:
            tax = [PRE, UNK, UNK] # Very bad format - can't tell PRE from FAM
        return tax

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[3] == "Gen" or tokens[3].islower() or tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            tax = [PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, UNK, UNK] # Bad format
        return tax
