from claravy.taxonomy import *


class Parse_Gridinsoft:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK!.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.TOK!TOK-TOK": self.parse_delim_fmt5,
            "TOK.TOK_TOK.TOK!TOK": self.parse_delim_fmt6,
        }

    # TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, UNK, UNK, UNK]
        if len(tokens[2]) == 1:
            tax = [CAT, FAM, SUF, SUF, SUF]
        elif tokens[1].startswith("Win"):
            tax = [CAT, FILE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [CAT, FILE, FAM, SUF]
        if len(tokens[1]) == 1:
            tax = [CAT, SUF, FAM, SUF]
        return tax

    # TOK.TOK!.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, SUF, SUF]

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT, FAM, SUF, SUF]

    #TOK.TOK.TOK.TOK!TOK-TOK
    def parse_delim_fmt5(self, tokens):
        return self.parse_delim_fmt2(tokens) + [SUF, SUF]

    # TOK.TOK_TOK.TOK!TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]
