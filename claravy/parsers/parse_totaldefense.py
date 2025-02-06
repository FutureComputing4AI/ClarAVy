from claravy.taxonomy import *


class Parse_Totaldefense: # Like etrustvet

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK!TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt3,
            "TOK/TOK": self.parse_delim_fmt4,
            "TOK/TOK_TOK": self.parse_delim_fmt5,
            "TOK/TOK.TOK.TOK[TOK]": self.parse_delim_fmt6,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF]

    # TOK/TOK!TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, FAM, SUF]

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt3(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK/TOK
    def parse_delim_fmt4(self, tokens):
        return [FILE, FAM]

    # TOK/TOK_TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF]

    # TOK/TOK.TOK.TOK[TOK]
    def parse_delim_fmt6(self, tokens):
        # Seems to be all Zango pinball malware? Unsure family
        return [FILE, UNK, UNK, SUF, SUF, NULL]
