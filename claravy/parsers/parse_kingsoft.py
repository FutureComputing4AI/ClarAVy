from claravy.taxonomy import *


class Parse_Kingsoft:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK.(TOK)": self.parse_delim_fmt1,
            "TOK.TOK.TOK.(TOK)": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK_TOK.TOK.(TOK)": self.parse_delim_fmt4,
            "TOK_TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
        }

    # TOK.TOK.TOK.TOK.(TOK)
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, PRE, UNK, SUF, SUF, NULL]
        if tokens[2].isnumeric():
            tax = [PRE, PRE, SUF, SUF, SUF, NULL]
        elif tokens[1].startswith("Heur"):
            tax = [PRE, PRE, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK.(TOK)
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, UNK, SUF, NULL]
        if len(tokens[2]) == 1 or tokens[2].islower():
            tax = [PRE, FAM, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, FAM, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if len(tokens[2]) == 1 or tokens[2].islower():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK_TOK.TOK.(TOK)
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[2] == "Heur" and tokens[3] == "Generic":
            tax = [PRE, PRE, PRE, PRE, SUF, SUF, NULL]
        elif tokens[3].isnumeric() or len(tokens[3]) <= 2:
            tax = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        elif tokens[3].islower():
            tax = [PRE, PRE, SUF, FAM, SUF, SUF, NULL]
        elif tokens[3].isupper():
            tax = [PRE, PRE, PRE, SUF, SUF, SUF, NULL]
        elif tokens[2].islower():
            tax = [PRE, PRE, SUF, FAM, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        return tax

    # TOK_TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE]                                                                        

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, CAT, FAM, SUF, SUF]
