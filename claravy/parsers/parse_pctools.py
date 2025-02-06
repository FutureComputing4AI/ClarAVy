from claravy.taxonomy import *


class Parse_Pctools:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK!TOK": self.parse_delim_fmt2,
            "TOK-TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK.TOK!TOK": self.parse_delim_fmt5,
        }

    # TOK.TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) <= 2 or tokens[1].lower() == "gen":
            if tokens[0].isupper():
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif tokens[1].isupper():
                tax = [PRE, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK!TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, FAM, SUF]

    # TOK-TOK.TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[2].isnumeric():
            tax = [UNK, UNK, SUF] # Bad format
        else:
            tax = [CAT, CAT, FAM]
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[0].isupper() or len(tokens[0]) <= 3:
                tax = [UNK, SUF, SUF]
            else:
                tax = [FAM, SUF, SUF]
        elif tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric() or tokens[2].lower() == "gen":
            if len(tokens[1]) <= 2 and tokens[1] != "VB":
                if tokens[0].isupper():
                    tax = [UNK, UNK, SUF] # Bad format
                else:
                    tax = [FAM, SUF, SUF]
            elif tokens[1].isupper() and tokens[1] != "VB":
                tax = [PRE, UNK, SUF] # Bad format
            else:
                tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, UNK, UNK] # Bad format
        return tax

    # TOK-TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        return [CAT, CAT, FAM, SUF]
