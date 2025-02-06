from claravy.taxonomy import *


class Parse_Sangfor:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK-TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK-TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK-TOK-TOK": self.parse_delim_fmt5,
        }

    # TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK.TOK-TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [CAT, PRE, PRE, PRE, SUF] # Save token - don't think it's a family

    # TOK.TOK.TOK-TOK
    def parse_delim_fmt4(self, tokens):
        return [FILE, CAT, FAM, SUF]

    # TOK.TOK.TOK-TOK-TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, CAT, FAM, SUF, SUF] 
