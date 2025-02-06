from claravy.taxonomy import *


class Parse_Catquickheal:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK": self.parse_delim_fmt4,
            "(TOK) - TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt7,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF]



    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].islower() or tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2] == "MUE": # Unsure of what this token is, but common
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[1].isupper():
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [UNK, SUF]
        elif tokens[1].isupper() and not any([c.isdigit() for c in tokens[1]]):
            tax = [PRE, UNK]
        elif tokens[1].islower():            
            tax = [UNK, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # (TOK) - TOK
    def parse_delim_fmt5(self, tokens):
        return [NULL, PRE, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, UNK, UNK, UNK, UNK]
        if tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[2] == "CVE" and tokens[3].isnumeric() and tokens[4].isnumeric():
            tax = [PRE, FAM, VULN, VULN, VULN]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        if tokens[2].isnumeric():
            tax = [UNK, UNK, SUF, SUF] # Bad format
        else:
            tax = [CAT, CAT, FAM, SUF]
        return tax

