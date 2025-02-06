from claravy.taxonomy import *


class Parse_Skyhigh:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK": self.parse_delim_fmt2,
            "TOK!TOK": self.parse_delim_fmt3,
            "TOK-TOK!TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK": self.parse_delim_fmt5,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, FILE, FAM, SUF]

    # TOK
    def parse_delim_fmt2(self, tokens):
        return [FAM]

    # TOK!TOK
    def parse_delim_fmt3(self, tokens):
        return [FAM, SUF]

    # TOK-TOK!TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[0].startswith("Generic"):
            tax = [SUF, SUF, SUF]
        elif tokens[1].isupper():
            tax = [UNK, SUF, SUF]
        return tax

    # TOK/TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF]

    #
    
    
    
    
