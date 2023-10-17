import re
from claravy.taxonomy import *


class Parse_Tencent:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK-TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK_TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK-TOK.TOK": self.parse_fmt5,
            "TOK.TOK.TOK": self.parse_fmt6,
            "TOK.TOK. TOK.TOK": self.parse_fmt7,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt8,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK-TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK_TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, PRE, SUF, PRE, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3] == "Gen" or len(tokens[3]) <= 2:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK-TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [TGT, CAT, UNK, UNK, SUF]
        if re.match(r"^Ms[0-9]+", tokens[2]) and tokens[3].isnumeric():
            fmt = [TGT, CAT, VULN, VULN, SUF]
        elif tokens[3] == "based":
            fmt = [TGT, CAT, FAM, SUF, SUF]
        elif tokens[2].lower() == "ps" and tokens[3].lower() == "mpc":
            fmt = [TGT, CAT, FAM, FAM, SUF]
        elif len(tokens[2]) <= 2:
            fmt = [TGT, CAT, SUF, FAM, SUF]
        elif tokens[3].isnumeric():
            fmt = [TGT, CAT, FAM, SUF, SUF]
        else:
            fmt = [TGT, CAT, UNK, UNK, SUF] # Bad format
        return fmt

    # TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        if len(tokens[0]) == 1:
            fmt = [SUF, PRE, FAM]
        elif len(tokens[2]) == 1 or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK. TOK.TOK
    def parse_fmt7(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF]
    
