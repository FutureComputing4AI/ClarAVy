from claravy.taxonomy import *


class Parse_Avastmobile: # Same company as Avast

    def __init__(self):
        self.parse_fmt = {
            "TOK:TOK-TOK [TOK]": self.parse_fmt1,
            "TOK:TOK [TOK]": self.parse_fmt2,
        }

    # TOK:TOK-TOK [TOK]
    def parse_fmt1(self, tokens):
        return [TGT, FAM, SUF, CAT, NULL]

    # TOK:TOK [TOK]
    def parse_fmt2(self, tokens):
        return [TGT, PRE, CAT, NULL]
