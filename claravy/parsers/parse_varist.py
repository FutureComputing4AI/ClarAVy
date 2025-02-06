from claravy.taxonomy import *


class Parse_Varist:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK-TOK 142945": self.parse_delim_fmt2,
            "TOK/TOK-TOK!TOK": self.parse_delim_fmt3,
            "TOK/TOK_TOK.TOK.TOK!TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK-TOK": self.parse_delim_fmt6,
        }

    # TOK/TOK.TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK-TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK-TOK!TOK
    def parse_delim_fmt3(self, tokens):
        tax = [FILE, UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            tax = [FILE, SUF, SUF, SUF]
        return tax

    # TOK/TOK_TOK.TOK.TOK!TOK
    def parse_delim_fmt4(self, tokens):
        return [FILE, FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF]

    # TOK.TOK-TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, SUF, SUF]
            
