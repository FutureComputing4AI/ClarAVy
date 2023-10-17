import re
from claravy.taxonomy import *


class Parse_Mcafee: # Mcafee, Mcafeegwedition both part of Mcafee

    def __init__(self):
        self.parse_fmt = {
            "TOK!TOK": self.parse_fmt1,
            "TOK/TOK.TOK": self.parse_fmt2,
            "TOK-TOK": self.parse_fmt3,
            "TOK-TOK!TOK": self.parse_fmt4,
            "TOK/TOK.TOK!TOK": self.parse_fmt5,
            "TOK-TOK.TOK": self.parse_fmt6,
            "TOK TOK.TOK": self.parse_fmt7,
            "TOK/TOK.TOK.TOK": self.parse_fmt8,
            "TOK-TOK.TOK.TOK": self.parse_fmt9,
            "TOK/TOK": self.parse_fmt10,
            "TOK": self.parse_fmt11,
            "TOK/TOK-TOK.TOK": self.parse_fmt12,
            "TOK.TOK": self.parse_fmt13,
            "TOK.TOK!TOK": self.parse_fmt14,
            "TOK.TOK.TOK": self.parse_fmt15,
            "TOK-TOK-TOK": self.parse_fmt16,
            "TOK/TOK.TOK.TOK!TOK": self.parse_fmt17,
            "TOK TOK.TOK!TOK": self.parse_fmt18,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt19,
            "TOK TOK!TOK": self.parse_fmt20,
            "TOK!TOK.TOK": self.parse_fmt21,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt22,
            "TOK/TOK-TOK": self.parse_fmt23,
        }

    # TOK!TOK
    def parse_fmt1(self, tokens):
        return [FAM, SUF]

    # TOK/TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            fmt = [PRE, SUF, SUF]
        else:
            fmt = [UNK, FAM, SUF] # Is tokens[0] CAT or TGT?
        return fmt

    # TOK-TOK
    def parse_fmt3(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isupper() or tokens[1].isnumeric() or tokens[1] == "Packed":
            fmt = [FAM, SUF]
        else:
            fmt = [CAT, FAM]
        return fmt

    # TOK-TOK!TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK, SUF]
        if re.match(r"^Generic[A-Z]+$", tokens[0]):
            fmt = [SUF, SUF, SUF]
        elif tokens[1].isupper():
            fmt = [FAM, SUF, SUF]
        elif tokens[1].islower() or tokens[1].isnumeric(): # Bad format
            fmt = [UNK, SUF, SUF]
        elif tokens[1] == "Gen":
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [CAT, FAM, SUF]
        return fmt

    # TOK/TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK-TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [CAT, UNK, UNK]
        if tokens[2].islower():
            if tokens[1].isupper() and len(tokens[1]) <= 3 and tokens[1] != "VB":
                fmt = [CAT, SUF, SUF]
            else:
                fmt = [CAT, FAM, SUF]
        else:
            fmt = [CAT, UNK, UNK] # Bad format
        return fmt

    # TOK TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[2].isnumeric():
            fmt = [FAM, FAM, UNK]
        else:
            fmt = [UNK, UNK, SUF] # Rarely [FAM, FAM, SUF] but usually [PRE, PRE, SUF]
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt8(self, tokens):
        fmt = [TGT, UNK, UNK, SUF]
        if tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            fmt = [TGT, FAM, SUF, SUF]
        else:
            fmt = [TGT, PRE, FAM, SUF]
        return fmt

    # TOK-TOK.TOK.TOK
    def parse_fmt9(self, tokens):
        if tokens[2].islower():
            if tokens[1].isupper():
                fmt = [CAT, UNK, SUF, SUF] # Bad format, usually SUF
            else:
                fmt = [CAT, FAM, SUF, SUF]
        else:
            fmt = [PRE, UNK, UNK, SUF] # Rare bad format
        return fmt

    # TOK/TOK
    def parse_fmt10(self, tokens):
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [TGT, SUF]
        elif tokens[1].isupper() or tokens[1].islower():
            fmt = [TGT, UNK] # Bad format
        else:
            fmt = [TGT, FAM]
        return fmt

    # TOK
    def parse_fmt11(self, tokens):
        return [FAM]

    # TOK/TOK-TOK.TOK
    def parse_fmt12(self, tokens):
        fmt = [TGT, CAT, UNK, SUF]
        if tokens[2].islower():
            fmt = [TGT, CAT, SUF, SUF]
        elif tokens[2].isupper() and not any([c.isdigit() for c in tokens[2]]):
            fmt = [TGT, CAT, SUF, SUF]
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt13(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower() or tokens[1].isupper():
            fmt = [FAM, SUF]
        else:
            fmt = [UNK, UNK] # Bad format
        return fmt

    # TOK.TOK!TOK
    def parse_fmt14(self, tokens):
        return self.parse_fmt13(tokens) + [SUF]

    # TOK.TOK.TOK
    def parse_fmt15(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[1].islower():
            fmt = [FAM, SUF, SUF]
        elif tokens[1].isnumeric():
            if tokens[2].islower():
                fmt = [FAM, SUF, SUF]
            else:
                fmt = [UNK, SUF, UNK] # Bad format
        else:
            fmt = [UNK, UNK, SUF] # Bad format
        return fmt

    # TOK-TOK-TOK
    def parse_fmt16(self, tokens):
        fmt = [UNK, UNK, UNK]
        if re.match(r"^CVE[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN]
        elif re.match(r"^MS[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN]
        elif tokens[1].isupper():
            fmt = [PRE, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK.TOK!TOK
    def parse_fmt17(self, tokens):
        return [TGT, FAM, PRE, SUF, SUF]

    # TOK TOK.TOK!TOK
    def parse_fmt18(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt19(self, tokens):
        return [TGT, FAM, UNK, SUF, SUF] # tokens[2] either CAT or SUF

    # TOK TOK!TOK
    def parse_fmt20(self, tokens):
        return [PRE, FAM, SUF]

    # TOK!TOK.TOK
    def parse_fmt21(self, tokens):
        return [FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt22(self, tokens):
        return self.parse_fmt9(tokens) + [SUF]

    # TOK/TOK-TOK
    def parse_fmt23(self, tokens):
        fmt = [TGT, CAT, UNK]
        if tokens[2].islower():
            fmt = [TGT, CAT, SUF]
        elif tokens[2].isupper() and not any([c.isdigit() for c in tokens[2]]):
            fmt = [TGT, CAT, SUF]
        else:
            fmt = [TGT, CAT, FAM]
        return fmt

    
