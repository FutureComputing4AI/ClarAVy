from claravy.taxonomy import *


class Parse_Sentinelone:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK - TOK TOK": self.parse_delim_fmt1,
            "TOK TOK - TOK": self.parse_delim_fmt2,
            "TOK TOK - TOK TOK": self.parse_delim_fmt3,
        }

    # TOK - TOK TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, PRE, FILE]

    # TOK TOK - TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, PRE]

    # TOK TOK - TOK TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, PRE, FILE]
