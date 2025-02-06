from claravy.taxonomy import *


class Parse_Vba32:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK-TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK.TOK-TOK.TOK": self.parse_delim_fmt7,
            "TOK-TOK.TOK": self.parse_delim_fmt8,
            "TOK TOK TOK.TOK.TOK.TOK": self.parse_delim_fmt9,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[2].isnumeric():
            if len(tokens[1]) <= 2 and tokens[1] != "VB":
                tax = [PRE, SUF, SUF]
            elif len(tokens[1]) == 3 and tokens[1].isupper():
                tax = [PRE, UNK, SUF] # Bad format
            else:
                tax = [PRE, FAM, SUF]
        elif tokens[2].islower():
            tax = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            tax = [PRE, UNK, UNK] # Bad format
        elif tokens[2] == "Heur":
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[0].isupper() or len(tokens[0]) <= 3:
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif tokens[1].islower():
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3].isupper() or len(tokens[3]) <= 2:
            if tokens[2].isupper() and tokens[2] != "VB":
                tax = [PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 4 and tokens[3].endswith("en"): # Gen, Sen, cGen
            if tokens[2].isupper() and tokens[2] != "VB":
                tax = [PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        elif tokens[3] == "Heur":
            tax = [PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM]
        return tax

    # TOK.TOK-TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if tokens[4].isnumeric() or tokens[4].isupper() or tokens[4].islower():
            if tokens[3].isupper():
                tax = [PRE, PRE, PRE, UNK, SUF] # Bad format
            else:
                tax = [PRE, CAT, CAT, FAM, SUF]
        elif len(tokens[4]) <= 3 or tokens[3] != "Win32":
            tax = [PRE, PRE, PRE, UNK, UNK] # Bad format
        else:
            tax = [PRE, CAT, CAT, FILE, FAM] # Only Win32 left
        return tax

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [CAT, CAT, UNK, UNK, SUF]
        if tokens[3] == "gen":
            tax = [CAT, CAT, FAM, SUF, SUF]
        else:
            tax = [CAT, CAT, FILE, FAM, SUF]
        return tax

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [CAT, CAT, UNK, UNK]
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "gen":
            if tokens[2].isupper() and len(tokens[2]) <= 3 and tokens[2] != "VB":
                tax = [CAT, CAT, UNK, UNK] # Bad format
            else:
                tax = [CAT, CAT, FAM, SUF]
        elif len(tokens[3]) <= 3:
            tax = [CAT, CAT, UNK, UNK] # Bad format
        else:
            tax = [CAT, CAT, PRE, FAM]
        return tax

    # TOK.TOK-TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, CAT, CAT, UNK]
        if tokens[3].isnumeric() or tokens[3].islower():
            tax = [PRE, CAT, CAT, SUF]
        elif tokens[3].isupper():
            tax = [PRE, CAT, CAT, UNK] # Bad format
        else:
            tax = [PRE, CAT, CAT, FAM]
        return tax

    # TOK-TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[1] == "based":
            tax = [PRE, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower():
            tax = [PRE, CAT, SUF]
        elif tokens[2].isupper():
            tax = [PRE, CAT, UNK] # Bad format
        else:
            tax = [PRE, CAT, FAM]
        return tax

    # TOK TOK TOK.TOK.TOK.TOK
    def parse_delim_fmt9(self, tokens):
        tax = [PRE, PRE, PRE, PRE, UNK, UNK]
        if tokens[5].isnumeric() or tokens[5].isupper() or tokens[5].islower():
            tax = [PRE, PRE, PRE, PRE, FAM, UNK]
        elif len(tokens[5]) <= 2 and tokens[5] != "VB":
            tax = [PRE, PRE, PRE, PRE, FAM, UNK]
        else:
            tax = [PRE, PRE, PRE, PRE, PRE, FAM]
        return tax
