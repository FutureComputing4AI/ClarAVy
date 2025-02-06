from claravy.taxonomy import *


class Parse_Cyren: # Renamed from Commtouch to Cyren, Acquired F-prot

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK!TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt3,
            "TOK/TOK-TOK!TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK-TOK": self.parse_delim_fmt5,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK/TOK": self.parse_delim_fmt7,
            "TOK/TOK_TOK.TOK.TOK!TOK": self.parse_delim_fmt8,
            "TOK.TOK": self.parse_delim_fmt9,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF]

    # TOK/TOK.TOK.TOK!TOK"
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt3(self, tokens):
        if tokens[3] == "Olympus":
            tax = [FILE, PRE, SUF, SUF]
        else:
            tax = [FILE, FAM, SUF, SUF]
        return tax

    # TOK/TOK-TOK!TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            tax = [PRE, SUF, SUF, SUF]
        elif tokens[1] == "Heuristic":
            if tokens[2].isupper() or tokens[2].isnumeric():
                tax = [PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        elif tokens[2] == "based":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].islower() or tokens[2].isupper():
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK-TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK
    def parse_delim_fmt7(self, tokens):
        return [FILE, FAM]

    # TOK/TOK_TOK.TOK.TOK!TOK
    def parse_delim_fmt8(self, tokens):
        return [FILE, UNK, UNK, SUF, SUF, SUF] # Bad format

    # TOK.TOK
    def parse_delim_fmt9(self, tokens):
        if tokens[1] == "gen":
            tax = [PRE, SUF]
        elif tokens[1].isnumeric() or len(tokens[1]) <= 2:
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax
