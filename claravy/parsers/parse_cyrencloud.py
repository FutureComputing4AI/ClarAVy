from claravy.taxonomy import *


class Parse_Cyrencloud: # Cloud version of Cyren. Related to Commtouch, F-Prot

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK-TOK": self.parse_delim_fmt3,
        }

    # TOK/TOK.TOK.TOK!TOK"
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF, SUF, SUF]

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt2(self, tokens):
        tax = [FILE, UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            tax = [FILE, SUF, SUF, SUF]
        return tax

     # TOK/TOK.TOK-TOK
    def parse_delim_fmt3(self, tokens):
        return [FILE, FAM, SUF, SUF]
