from claravy.taxonomy import *


class Parse_Bytehero:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK-TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, UNK, FAM, SUF]
        if tokens[1] == "Exception":
            tax = [CAT, PRE, FAM, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK"
    def parse_delim_fmt2(self, tokens):
        return [CAT, PRE, FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT, CAT, PRE, FAM, SUF]
