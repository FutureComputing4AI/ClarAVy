from claravy.taxonomy import *


class Parse_Baidu: # Same company as Baiduinternational. Possibly related to Tencent, but unclear. May use Avira engine, but label formats seem unrelated.

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK-TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [TGT, UNK, UNK, SUF]
        if tokens[1] == "Packed":
            fmt = [TGT, PRE, PACK, SUF]
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK.TOK-TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [TGT, PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE]
