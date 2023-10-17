from claravy.taxonomy import *


class Parse_Baiduinternational: # Same company as Baidu

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.$TOK": self.parse_fmt2,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [TGT, CAT, FAM, SUF]

    # TOK.TOK.TOK.$TOK
    def parse_fmt2(self, tokens):
        return [TGT, CAT, FAM, SUF]
