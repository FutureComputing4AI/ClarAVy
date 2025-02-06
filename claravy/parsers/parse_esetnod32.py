from claravy.taxonomy import *


class Parse_Esetnod32: # Renamed from nod32

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK TOK TOK TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK TOK TOK TOK/TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK TOK TOK TOK/TOK.TOK TOK TOK": self.parse_delim_fmt5,
            "TOK/TOK.TOK TOK TOK": self.parse_delim_fmt6,
            "TOK TOK TOK TOK/TOK.TOK.TOK TOK TOK": self.parse_delim_fmt7,
            "TOK/TOK": self.parse_delim_fmt8,
            "TOK TOK TOK TOK/TOK": self.parse_delim_fmt9,
            "TOK TOK TOK TOK TOK/TOK.TOK": self.parse_delim_fmt10,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF]

    # TOK TOK TOK TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, PRE, FILE, FAM, SUF]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [FILE, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            tax = [FILE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [FILE, FAM, SUF, SUF]
        elif tokens[2].isupper() and len(tokens[2]) == 3:
            tax = [FILE, UNK, UNK, SUF] # Bad format
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK TOK TOK TOK/TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE] + self.parse_delim_fmt3(tokens[3:])

    # TOK TOK TOK TOK/TOK.TOK TOK TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, PRE, FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK TOK TOK
    def parse_delim_fmt6(self, tokens):
        return [FILE, FAM, SUF, SUF, SUF]

    # TOK TOK TOK TOK/TOK.TOK.TOK TOK TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, PRE, PRE, FILE, UNK, UNK, SUF, SUF, SUF]
        if tokens[5].isupper():
            tax = [PRE, PRE, PRE, FILE, FAM, SUF, SUF, SUF, SUF]
        elif tokens[4] == "FlyStudio":
            tax = [PRE, PRE, PRE, FILE, FAM, SUF, SUF, SUF, SUF] # Bad format - only for FlyStudio
        else:
            tax = [PRE, PRE, PRE, FILE, CAT, FAM, SUF, SUF, SUF]
        return tax

    # TOK/TOK
    def parse_delim_fmt8(self, tokens):
        return [FILE, FAM]

    # TOK TOK TOK TOK/TOK
    def parse_delim_fmt9(self, tokens):
        return [PRE, PRE, PRE, FILE, FAM]

    # TOK TOK TOK TOK TOK/TOK.TOK
    def parse_delim_fmt10(self, tokens):
        return [PRE, PRE, PRE, PRE, FILE, FAM, SUF]
