import re
from claravy.taxonomy import *


class Parse_Gdata: # Uses Bitdefender and in-house engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK-TOK.TOK.TOK": self.parse_fmt5,
            "TOK:TOK-TOK ": self.parse_fmt6,
            "TOK.TOK.TOK.TOK@TOK": self.parse_fmt7,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_fmt8,
            "TOK:TOK.TOK.TOK@TOK": self.parse_fmt9,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_fmt10,
            "TOK:TOK-TOK": self.parse_fmt11,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt12,
            "TOK.TOK-TOK.TOK.TOK@TOK": self.parse_fmt13,
            "TOK.TOK.TOK!.TOK": self.parse_fmt14,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic":
            fmt = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric() or len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Generic" and tokens[1] == "Malware":
            fmt = [PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        if tokens[1] == "Packer":
            if len(tokens[3]) == 1:
                fmt = [PRE, PRE, PACK, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, PACK, SUF]
        if tokens[2] == "Generic":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[2] == "Malware":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            fmt = [PRE, CAT, FAM, SUF, SUF]
        elif tokens[3].isupper() and tokens[3] != "VB":
            fmt = [PRE, CAT, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK-TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        return [TGT, CAT, CAT, FAM, SUF]

    # TOK:TOK-TOK
    def parse_fmt6(self, tokens):
        return [PRE, FAM, SUF, NULL]

    # TOK.TOK.TOK.TOK@TOK
    def parse_fmt7(self, tokens):
        fmt = [PRE, PRE, UNK, SUF, SUF]
        if tokens[2] == "Heur":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        fmt = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[4].isnumeric() or len(tokens[4]) == 1:
            if tokens[3].isnumeric() or len(tokens[3]) == 1:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if (tokens[4].isupper() and tokens[4] != "VB") or tokens[4] == "Gen":
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK@TOK
    def parse_fmt9(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_fmt10(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK:TOK-TOK
    def parse_fmt11(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt12(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if re.match(r"^M[Ss][0-9]+$", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK-TOK.TOK.TOK@TOK
    def parse_fmt13(self, tokens):
        return [TGT, CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!.TOK
    def parse_fmt14(self, tokens):
        return [PRE, PRE, SUF, SUF]
