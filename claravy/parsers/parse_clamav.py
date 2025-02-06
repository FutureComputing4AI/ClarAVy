from claravy.taxonomy import *


class Parse_Clamav:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK-TOK": self.parse_delim_fmt1,
            "TOK.TOK-TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK-TOK-TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK-TOK-TOK-TOK": self.parse_delim_fmt5,
            "TOK.TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt7,
        }

    # TOK.TOK.TOK-TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[1] == "Packed":
            tax = [PRE, PRE, PACK, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, CAT, FAM, SUF]
        return tax

    # TOK.TOK-TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK-TOK-TOK
    def parse_delim_fmt3(self, tokens):
        return [FILE, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if tokens[1] == "Packed":
            tax = [PRE, PRE, PACK]
        elif tokens[2].isnumeric():
            if tokens[1].isnumeric():
                if tokens[0].isupper():
                    tax = [SUF, SUF, SUF]
                else:
                    tax = [FAM, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2:
            if tokens[1].isnumeric():
                tax = [FAM, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF]
        elif tokens[2].lower() == "gen":
            tax = [PRE, FAM, SUF]
        elif tokens[2].isupper(): # Bad format
            tax = [PRE, UNK, UNK]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK-TOK-TOK-TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric() or tokens[1].islower():
            if len(tokens[0]) <= 2 and tokens[0] != "VB":
                tax = [SUF, SUF]
            else:
                tax = [FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        if tokens[1] == "Packed":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[3].isupper() or tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            tax = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            tax = [PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM]
        return tax

