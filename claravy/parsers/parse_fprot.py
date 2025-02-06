from claravy.taxonomy import *


class Parse_Fprot: # Acquired by Commtouch/Cyren

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK-TOK!TOK": self.parse_delim_fmt3,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK": self.parse_delim_fmt6,
            "TOK/TOK": self.parse_delim_fmt7,
            "TOK/TOK.TOK@TOK": self.parse_delim_fmt8,
            "TOK/TOK_TOK.TOK.TOK!TOK": self.parse_delim_fmt9,
        }

    # TOK/TOK.TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF]

    # TOK/TOK-TOK!TOK
    def parse_delim_fmt3(self, tokens):
        tax = [FILE, UNK, SUF, SUF]
        if len(tokens[1]) == 1:
            tax = [FILE, SUF, SUF, SUF]
        elif tokens[1].isupper():
            tax = [FILE, PRE, FAM, SUF]
        else:
            tax = [FILE, FAM, SUF, SUF]
        return tax

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt4(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK.TOK
    def parse_delim_fmt6(self, tokens):
        if tokens[1] == "gen":
            tax = [PRE, SUF]
        elif tokens[1].isnumeric() or len(tokens[1]) <= 2:
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK/TOK
    def parse_delim_fmt7(self, tokens):
        return [FILE, FAM]

    # TOK/TOK.TOK@TOK
    def parse_delim_fmt8(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK_TOK.TOK.TOK!TOK
    def parse_delim_fmt9(self, tokens):
        return [FILE, UNK, UNK, SUF, SUF, SUF] # Bad format
