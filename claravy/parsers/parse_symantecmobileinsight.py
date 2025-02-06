from claravy.taxonomy import *


class Parse_Symantecmobileinsight:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK": self.parse_delim_fmt1,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt2,
        }

    # TOK:TOK
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, UNK]
        if tokens[1].startswith("Gen"):
            tax = [CAT, SUF]
        else:
            tax = [CAT, FAM]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FILE, FAM, SUF]
