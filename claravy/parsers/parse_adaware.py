import re
from claravy.taxonomy import *


class Parse_Adaware: # Uses Bitdefender engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK:TOK.TOK.TOK@TOK": self.parse_fmt6,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt7,
            "TOK.TOK.TOK!.TOK": self.parse_fmt8,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_fmt9,
            "TOK.TOK.TOK@TOK": self.parse_fmt10,
            "TOK.TOK": self.parse_fmt11,
            "TOK.TOK-TOK.TOK": self.parse_fmt12,
            "TOK.TOK.TOK!TOK!TOK.TOK": self.parse_fmt13,
            "TOK.TOK.TOK!TOK.TOK": self.parse_fmt14,
            "TOK:TOK.TOK.TOK!TOK.TOK": self.parse_fmt15,
            "TOK.TOK-TOK-TOK.TOK": self.parse_fmt16,
            "TOK:TOK.TOK.TOK@TOK!TOK": self.parse_fmt17,
            "TOK:TOK.TOK.TOK@TOK@TOK": self.parse_fmt18,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        if tokens[3].isnumeric() and tokens[2].startswith("b"):
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen" or tokens[2].isnumeric() or len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[1].isupper():
                fmt = [PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF]
        elif tokens[3] == "Gen" or tokens[3].isnumeric() or tokens[3].isupper():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, PRE, PRE, UNK, UNK, SUF]
        if tokens[4] == "Gen" or tokens[4].isnumeric() or (len(tokens[4]) <= 2 and tokens[4] != "VB"):
            if tokens[3].isnumeric() or len(tokens[3]) <= 2:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK@TOK
    def parse_fmt6(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK!.TOK
    def parse_fmt8(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_fmt9(self, tokens):
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

    # TOK.TOK.TOK@TOK
    def parse_fmt10(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK.TOK
    def parse_fmt11(self, tokens):
        fmt = [UNK, UNK]
        if len(tokens[1]) == 4 and tokens[1].isupper():
            fmt = [PRE, SUF]
        elif len(tokens[1]) <= 2 or tokens[1].isnumeric() or tokens[1] == "Gen":
            if tokens[0].isupper():
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif len(tokens[1]) == 3 and tokens[1].isupper():
            fmt = [PRE, UNK]
        elif re.match(r"^[0-9A-Z]+$", tokens[1]):
            fmt = [PRE, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK-TOK.TOK
    def parse_fmt12(self, tokens):
        # TODO: Lots of unusual formats in here
        return [UNK, UNK, UNK, SUF]

    # TOK.TOK.TOK!TOK!TOK.TOK
    def parse_fmt13(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_fmt14(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK.TOK
    def parse_fmt15(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK-TOK-TOK.TOK
    def parse_fmt16(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "CVE" and tokens[2].isnumeric() and tokens[3].isnumeric():
            fmt = [PRE, VULN, VULN, VULN, SUF]
        else:
            fmt = [PRE, PRE, PRE, PRE, SUF]
        return fmt

    # TOK:TOK.TOK.TOK@TOK!TOK
    def parse_fmt17(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK@TOK@TOK
    def parse_fmt18(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF]
