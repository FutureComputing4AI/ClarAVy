from claravy.taxonomy import *


class Parse_Baidu: # Same company as Baiduinternational. Possibly related to Tencent, but unclear. May use Avira engine, but label formats seem unrelated.

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK-TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [FILE, UNK, UNK, SUF]
        if tokens[1] == "Packed":
            tax = [FILE, PRE, PACK, SUF]
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK.TOK-TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [FILE, PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE]
