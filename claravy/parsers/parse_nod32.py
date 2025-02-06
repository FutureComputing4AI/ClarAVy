from claravy.taxonomy import *


class Parse_Nod32: # Renamed to Esetnod32

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK TOK TOK TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK TOK TOK TOK/TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK TOK TOK TOK TOK/TOK.TOK": self.parse_delim_fmt5,
        }

    # TOK TOK TOK TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, PRE, PRE, FILE, FAM, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[1] == "Packed":
            tax = [FILE, PRE, PACK, SUF]
        elif tokens[2].islower():
            tax = [FILE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [FILE, FAM, SUF, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            tax = [FILE, UNK, UNK, SUF]
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK TOK TOK TOK TOK/TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE, FILE, CAT, FAM, SUF]

    # TOK TOK TOK TOK TOK/TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, PRE, PRE, FILE, FAM, SUF]

