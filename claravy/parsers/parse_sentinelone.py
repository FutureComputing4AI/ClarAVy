from claravy.taxonomy import *


class Parse_Sentinelone:

    def __init__(self):
        self.parse_fmt = {
            "TOK - TOK TOK": self.parse_fmt1,
            "TOK TOK - TOK": self.parse_fmt2,
            "TOK TOK - TOK TOK": self.parse_fmt3,
        }

    # TOK - TOK TOK
    def parse_fmt1(self, tokens):
        return [PRE, PRE, TGT]

    # TOK TOK - TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE, PRE]

    # TOK TOK - TOK TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, PRE, TGT]
