from claravy.taxonomy import *


class Parse_Zonealarm: # Partnership with Kaspersky

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK-TOK-TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK-TOK-TOK:TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK-TOK-TOK:TOK:TOK.TOK.TOK": self.parse_delim_fmt7,
            "TOK:TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK:TOK-TOK.TOK.TOK": self.parse_delim_fmt9,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt10,
        }

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, CAT, FILE, FAM]

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK-TOK-TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE, CAT, FILE, FAM, SUF]

    # TOK-TOK-TOK:TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):

        return [PRE, PRE, PRE, PRE, CAT, FILE, FAM, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, CAT, FILE, FAM, SUF]

    # TOK-TOK-TOK:TOK:TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [PRE, PRE, PRE, PRE, CAT, FILE, FAM]

    # TOK:TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        return [PRE, CAT, CAT, FILE, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt9(self, tokens):
        if tokens[4] == "Generic":
            tax = [PRE, CAT, CAT, FILE, PRE]
        else:
            tax = [PRE, CAT, CAT, UNK, UNK] # Bad format
        return tax

    # TOK:TOK-TOK.TOK.TOK
    def parse_delim_fmt10(self, tokens):
        if tokens[3].isnumeric():
            if len(tokens[2]) <= 2 and tokens[2] != "VB":
                tax = [CAT, PRE, SUF, SUF, SUF]
            else:
                tax = [CAT, PRE, FAM, SUF, SUF]
        elif tokens[3].islower() and not any([c.isdigit() for c in tokens[3]]):
            tax = [CAT, FILE, FAM, SUF, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            if tokens[2].isupper():
                tax = [CAT, FILE, UNK, SUF, SUF] # Bad format
            else:
                tax = [CAT, FILE, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, UNK, UNK, SUF] # Bad format
        return tax
