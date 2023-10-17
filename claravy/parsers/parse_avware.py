import re
from claravy.taxonomy import *


class Parse_Avware: # Uses Vipre engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK (TOK)": self.parse_fmt1,
            "TOK.TOK.TOK!TOK": self.parse_fmt2,
            "TOK.TOK.TOK (TOK)": self.parse_fmt3,
            "TOK (TOK)": self.parse_fmt4,
            "TOK-TOK.TOK.TOK.TOK (TOK)": self.parse_fmt5,
            "TOK-TOK.TOK.TOK (TOK)": self.parse_fmt6,
            "TOK.TOK.TOK.TOK!TOK": self.parse_fmt7,
            "TOK.TOK.TOK!TOK.TOK": self.parse_fmt8,
            "TOK.TOK": self.parse_fmt9,
            "TOK": self.parse_fmt10,
            "TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_fmt11,
            "TOK/TOK (TOK)": self.parse_fmt12,
            "TOK TOK (TOK)": self.parse_fmt13,
            "TOK.TOK.TOK": self.parse_fmt14,
            "TOK.TOK.TOK.TOK!TOK (TOK)": self.parse_fmt15,
            "TOK.TOK (TOK)": self.parse_fmt16,
            "TOK.TOK.TOK.TOK (TOK-TOK)": self.parse_fmt17,
            "TOK TOK. (TOK)": self.parse_fmt18,
            "TOK.TOK.TOK!TOK (TOK)": self.parse_fmt19,
            "TOK.TOK.TOK-TOK (TOK)": self.parse_fmt20,
            "TOK-TOK.TOK.TOK": self.parse_fmt21,
            "TOK.TOK.TOK-TOK-TOK (TOK)": self.parse_fmt22,
            "TOK.TOK.TOK-TOK-TOK.TOK (TOK)": self.parse_fmt23
        }

    # TOK.TOK.TOK.TOK (TOK) 
    def parse_fmt1(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, SUF, NULL]
        if tokens[2] == "Packer":
            fmt = [CAT, TGT, PRE, PACK, SUF, NULL]
        else:
            fmt = [CAT, TGT, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK!TOK
    def parse_fmt2(self, tokens):
        if tokens[2] == "Generic":
            fmt = [PRE, PRE, PRE, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK (TOK)
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF, NULL]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF, SUF, NULL]
        elif len(tokens[2]) <= 2 or tokens[2].lower() == "gen":
            fmt = [PRE, FAM, SUF, SUF, NULL]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, NULL]
        else:
            fmt = [PRE, TGT, FAM, SUF, NULL]
        return fmt

    # TOK (TOK)
    def parse_fmt4(self, tokens):
        return [FAM, SUF, NULL]

    # TOK-TOK.TOK.TOK.TOK (TOK)
    def parse_fmt5(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, SUF, NULL]

    # TOK-TOK.TOK.TOK (TOK)
    def parse_fmt6(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, NULL]

    # TOK.TOK.TOK.TOK!TOK
    def parse_fmt7(self, tokens):
        return [CAT, TGT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_fmt8(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]

    # TOK.TOK
    def parse_fmt9(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower():
            fmt = [FAM, SUF]
        else:
            fmt = [UNK, FAM]
        return fmt

    # TOK
    def parse_fmt10(self, tokens):
        return [FAM]

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_fmt11(self, tokens):
        return [CAT, TGT, FAM, SUF, SUF, SUF, NULL]

    # TOK/TOK (TOK)
    def parse_fmt12(self, tokens):
        return [FAM, FAM, SUF, NULL]

    # TOK TOK (TOK)
    def parse_fmt13(self, tokens):
        if tokens[0] == "Corrupted":
            fmt = [PRE, PRE, SUF, NULL]
        else:
            fmt = [FAM, FAM, SUF, NULL]
        return fmt

    # TOK.TOK.TOK
    def parse_fmt14(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[2] == "gen":
            fmt = [PRE, PRE, SUF]
        elif tokens[2].isupper() or tokens[2].islower(): # Bad format
            fmt = [PRE, UNK, UNK]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK!TOK (TOK)
    def parse_fmt15(self, tokens):
        return [CAT, TGT, FAM, SUF, SUF, SUF, NULL]

    # TOK.TOK (TOK)
    def parse_fmt16(self, tokens):
        fmt = [UNK, UNK, SUF, NULL]
        if tokens[1].islower() or len(tokens[1]) == 1 or tokens[1] == "Gen":
            fmt = [FAM, SUF, SUF, NULL]
        else:
            fmt = [PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK.TOK (TOK-TOK)
    def parse_fmt17(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF, NULL]

    # TOK TOK. (TOK)
    def parse_fmt18(self, tokens):
        return [FAM, FAM, SUF, NULL]

    # TOK.TOK.TOK!TOK (TOK)
    def parse_fmt19(self, tokens):
        fmt = [PRE, UNK, UNK, SUF, SUF, SUF]
        if len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        return fmt

    # TOK.TOK.TOK-TOK (TOK)
    def parse_fmt20(self, tokens):
        fmt = []
        if re.match(r"^CVE[0-9]{4}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, SUF, NULL]
        elif tokens[2].islower() or len(tokens[2]) <= 2:
            fmt = [PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, TGT, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK-TOK (TOK)
    def parse_fmt21(self, tokens):
        fmt = [UNK, CAT, UNK, UNK]
        if tokens[3].isupper() or tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            fmt = [PRE, CAT, FAM, SUF]
        else:
            fmt = [CAT, CAT, TGT, FAM]
        return fmt

    # TOK.TOK.TOK-TOK-TOK (TOK)
    def parse_fmt22(self, tokens):
        return [PRE, TGT, VULN, VULN, VULN, SUF, NULL]

    # TOK.TOK.TOK-TOK-TOK.TOK (TOK)
    def parse_fmt23(self, tokens):
        return [PRE, TGT, VULN, VULN, VULN, SUF, SUF, NULL]

