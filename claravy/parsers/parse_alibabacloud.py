import re
from claravy.taxonomy import *


class Parse_Alibabacloud:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK[TOK]:TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK/TOK.TOK(TOK)": self.parse_delim_fmt3,
            "TOK": self.parse_delim_fmt4,
            "TOK:TOK/TOK.TOK!TOK": self.parse_delim_fmt5,
            #"TOK:TOK/TOK-TOK-TOK.TOK": self.parse_delim_fmt2,
            #"TOK:TOK/TOK_TOK.TOK": self.parse_delim_fmt3,
            #"TOK:TOK/TOK-TOK.TOK": self.parse_delim_fmt4,
            #"TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            #"TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            #"TOK:TOK/TOK_TOK_TOK.TOK": self.parse_delim_fmt7,
            #"TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt8,
        }

    # TOK:TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK[TOK]:TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK:TOK/TOK.TOK(TOK)
    def parse_delim_fmt3(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF, NULL]

    # TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT]

    # TOK:TOK/TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF]
