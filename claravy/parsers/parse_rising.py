import re
from claravy.taxonomy import *


class Parse_Rising:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK!TOK.TOK (TOK)": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK!TOK.TOK (TOK:TOK:TOK)": self.parse_fmt3,
            "TOK.TOK/TOK!TOK.TOK (TOK)": self.parse_fmt4,
            "TOK.TOK!TOK.TOK (TOK:TOK)": self.parse_fmt5,
            "TOK:TOK.TOK!TOK.TOK": self.parse_fmt6,
            "TOK:TOK.TOK.TOK.TOK!TOK": self.parse_fmt7,
            "TOK.TOK.TOK.TOK (TOK)": self.parse_fmt8,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt9,
            "TOK.TOK@TOK!TOK.TOK (TOK)": self.parse_fmt10,
            "TOK:TOK.TOK.TOK.TOK.TOK.TOK!TOK": self.parse_fmt11,
            "TOK.TOK!TOK": self.parse_fmt12,
            "TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_fmt13,
            "TOK.TOK.TOK.TOK (TOK:TOK)": self.parse_fmt14,
            "TOK.TOK.TOK": self.parse_fmt15,
            "TOK:TOK.TOK.TOK.TOK.TOK!TOK": self.parse_fmt16,
            "TOK.TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_fmt17,
            "TOK:TOK.TOK.TOK!TOK": self.parse_fmt18,
            "TOK.TOK-TOK!TOK.TOK (TOK:TOK:TOK)": self.parse_fmt19,
            "TOK:TOK.TOK-TOK/TOK!TOK.TOK": self.parse_fmt20,
            "TOK:TOK.TOK(TOK)!TOK.TOK [TOK]": self.parse_fmt21,
            "TOK:TOK.TOK!TOK.TOK [TOK]": self.parse_fmt22,
            "TOK.TOK@TOK.TOK (TOK:TOK)": self.parse_fmt23,
            "TOK:TOK.TOK@TOK!TOK.TOK": self.parse_fmt24,
            "TOK.TOK.TOK (TOK)": self.parse_fmt25,
            "TOK": self.parse_fmt26,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt27,
            "TOK:TOK.TOK/TOK!TOK.TOK [TOK]": self.parse_fmt28,
            "TOK.TOK.TOK!TOK": self.parse_fmt29,
            "TOK.TOK-TOK!TOK.TOK (TOK:TOK)": self.parse_fmt30,
        }

    # TOK.TOK!TOK.TOK (TOK)
    def parse_fmt1(self, tokens):
        fmt = [CAT, UNK, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            fmt = [CAT, VULN, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, FAM, SUF, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [CAT, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            fmt = [CAT, FAM, SUF, SUF]
        else:
            fmt = [CAT, PRE, FAM, SUF]
        return fmt

    # TOK.TOK!TOK.TOK (TOK:TOK:TOK)
    def parse_fmt3(self, tokens):
        fmt = [CAT, UNK, SUF, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            fmt = [CAT, VULN, SUF, SUF, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, FAM, SUF, SUF, SUF, SUF, SUF, NULL]
        return fmt

    # TOK.TOK/TOK!TOK.TOK (TOK)
    def parse_fmt4(self, tokens):
        if tokens[2].isupper():
            fmt = [CAT, FAM, PRE, SUF, SUF, SUF, NULL]
        elif tokens[1].isupper():
            fmt = [CAT, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, UNK, UNK, SUF, SUF, SUF, NULL] # Bad format
        return fmt

    # TOK.TOK!TOK.TOK (TOK:TOK)
    def parse_fmt5(self, tokens):
        fmt = [CAT, UNK, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            fmt = [CAT, VULN, SUF, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, FAM, SUF, SUF, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK!TOK.TOK
    def parse_fmt6(self, tokens):
        return [TGT, CAT, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK!TOK
    def parse_fmt7(self, tokens):
        fmt = [PRE, PRE, PRE, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PRE, PACK, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK.TOK (TOK)
    def parse_fmt8(self, tokens):
        fmt = [UNK, UNK, UNK, SUF, SUF, NULL]
        if tokens[2].isnumeric():
            if tokens[1].isupper():
                fmt = [UNK, UNK, UNK, SUF, SUF, NULL] # Bad format
            else:
                fmt = [CAT, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt9(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                fmt = [PRE, PRE, UNK, SUF, SUF] # Bad format
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [CAT, PRE, TGT, FAM, SUF]
        return fmt

    # TOK.TOK@TOK!TOK.TOK (TOK)
    def parse_fmt10(self, tokens):
        return [PRE, FAM, SUF, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK.TOK.TOK.TOK.TOK!TOK
    def parse_fmt11(self, tokens):
        return [TGT, CAT, CAT, PRE, TGT, FAM, SUF, SUF]

    # TOK.TOK!TOK
    def parse_fmt12(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_fmt13(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                fmt = [PRE, PRE, UNK, SUF, SUF, SUF, NULL] # Bad format
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, PRE, TGT, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK (TOK:TOK)
    def parse_fmt14(self, tokens):
        fmt = [CAT, UNK, UNK, SUF, SUF, SUF, NULL]
        if tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
        elif tokens[3].islower() or tokens[3] == "GEN":
            fmt = [CAT, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, PRE, PRE, SUF, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK
    def parse_fmt15(self, tokens):
        if tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            if tokens[2].isnumeric() or len(tokens[2]) <= 2:
                fmt = [FAM, SUF, SUF]
            else:
                fmt = [CAT, PRE, FAM]
        elif tokens[2].islower() or tokens[2] == "GEN" or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt        

    # TOK:TOK.TOK.TOK.TOK.TOK!TOK
    def parse_fmt16(self, tokens):
        return [TGT, CAT, PRE, TGT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_fmt17(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                fmt = [PRE, PRE, UNK, SUF, SUF, SUF, SUF, NULL] # Bad format
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, PRE, PRE, TGT, FAM, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK.TOK!TOK
    def parse_fmt18(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3].islower() or tokens[3].isupper() or tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK-TOK!TOK.TOK (TOK:TOK:TOK)
    def parse_fmt19(self, tokens):
        fmt = [CAT, UNK, UNK, SUF, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            fmt = [CAT, VULN, VULN, SUF, SUF, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, CAT, FAM, SUF, SUF, SUF, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK-TOK/TOK!TOK.TOK
    def parse_fmt20(self, tokens):
        return [TGT, PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK(TOK)!TOK.TOK [TOK]
    def parse_fmt21(self, tokens):
        return [TGT, PRE, PRE, FAM, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK!TOK.TOK [TOK]
    def parse_fmt22(self, tokens):
        return [TGT, CAT, FAM, SUF, SUF, SUF, NULL]

    # TOK.TOK@TOK.TOK (TOK:TOK)
    def parse_fmt23(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK@TOK!TOK.TOK
    def parse_fmt24(self, tokens):
        return [TGT, PRE, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK (TOK)
    def parse_fmt25(self, tokens):
        return self.parse_fmt15(tokens) + [SUF, NULL]

    # TOK
    def parse_fmt26(self, tokens):
        fmt = [UNK]
        if tokens[0].isnumeric():
            fmt = [SUF]
        else:
            fmt = [FAM]
        return fmt

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt27(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                fmt = [PRE, PRE, UNK, SUF, SUF, SUF] # Bad format
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [CAT, PRE, PRE, TGT, FAM, SUF]
        return fmt

    # TOK:TOK.TOK/TOK!TOK.TOK [TOK]
    def parse_fmt28(self, tokens):
        return [TGT, PRE, FAM, UNK, SUF, SUF, SUF, NULL] # tokens[3] can be PRE, SUF, TGT

    # TOK.TOK.TOK!TOK
    def parse_fmt29(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK-TOK!TOK.TOK (TOK:TOK)
    def parse_fmt30(self, tokens):
        fmt = [CAT, UNK, UNK, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            fmt = [CAT, VULN, VULN, SUF, SUF, SUF, SUF, NULL]
        else:
            fmt = [CAT, CAT, FAM, SUF, SUF, SUF, SUF, NULL]
        return fmt
