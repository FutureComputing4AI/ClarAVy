from claravy.taxonomy import *


class Parse_Nprotect: # Renamed to Tachyon

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK-TOK/TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK-TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt7,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK/TOK.TOK": self.parse_delim_fmt9,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            tax = [PRE, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            if len(tokens[1]) == 1:
                tax = [FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic":
            tax = [PRE, PRE, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper():
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK-TOK/TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK-TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if len(tokens[3]) <= 2 and tokens[3].upper() != "VB":
            tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[3].isupper() and tokens[3] != "VB":
            tax = [PRE, PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK
    def parse_delim_fmt9(self, tokens):
        return [CAT, FILE, FAM]


