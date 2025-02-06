from claravy.taxonomy import *


class Parse_Bkav:

    # TODO: Need to fix famvt family! It's a prefix and there are other families in that label

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
        }


    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, UNK] # Last token either SUF or CAT

    # TOK.TOK.
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, NULL]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, UNK]
        if tokens[1].lower().startswith("fam"):
            if tokens[3] == "PE":
                tax = [FILE, PRE, FAM, FILE]
            else:
                tax = [FILE, PRE, FAM, CAT]
        elif tokens[1].startswith("Clod"):
            tax = [PRE, SUF, UNK, UNK]
        else:
            tax = [PRE, FAM, UNK, UNK]
        return tax

    # TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [UNK, FAM] # First token either SUF or FILE

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, UNK, UNK, UNK]
        if tokens[1].startswith("Fam"):
            if tokens[4] == "PE":
                tax = [FILE, PRE, FAM, SUF, FILE]
            else:
                tax = [FILE, PRE, FAM, SUF, CAT]
        else:
            tax = [FILE, CAT, FAM, SUF, SUF]
        return tax 
