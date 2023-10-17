import re
from claravy.taxonomy import *


class Parse_Mcafeegwedition: # Mcafee, Mcafeegwedition both part of Mcafee

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK!TOK": self.parse_fmt3,
            "TOK/TOK.TOK": self.parse_fmt4,
            "TOK/TOK.TOK!TOK": self.parse_fmt5,
            "TOK-TOK!TOK": self.parse_fmt6,
            "TOK.TOK.TOK.TOK-TOK.TOK": self.parse_fmt7,
            "TOK-TOK": self.parse_fmt8,
            "TOK-TOK.TOK.TOK": self.parse_fmt9,
            "TOK-TOK.TOK": self.parse_fmt10,
            "TOK TOK.TOK": self.parse_fmt11,
            "TOK": self.parse_fmt12,
            "TOK.TOK.TOK": self.parse_fmt13,
            "TOK/TOK.TOK.TOK": self.parse_fmt14,
            "TOK/TOK-TOK.TOK": self.parse_fmt15,
            "TOK/TOK": self.parse_fmt16,
            "TOK.TOK.TOK.TOK.TOK!TOK": self.parse_fmt17,
            "TOK.TOK": self.parse_fmt18,
            "TOK.TOK!TOK": self.parse_fmt19,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric():
            if len(tokens[2]) <= 2 or tokens[2].isnumeric() or tokens[2] == "Patched":
                fmt = [PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        elif tokens[2].islower() or tokens[2].isnumeric():
            if tokens[1].islower():
                fmt = [FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper(): # Bad format
            fmt = [PRE, PRE, UNK, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, PRE, TGT, FAM, SUF] # Very few (if any) actual families in FAM

    # TOK!TOK
    def parse_fmt3(self, tokens):
        return [FAM, SUF]

    # TOK/TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            fmt = [PRE, SUF, SUF]
        else:
            fmt = [TGT, FAM, SUF]
        return fmt

    # TOK/TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK-TOK!TOK
    def parse_fmt6(self, tokens):
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

    # TOK.TOK.TOK.TOK-TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [PRE, PRE, TGT, UNK, UNK, SUF]
        if re.match("^[M][Ss][0-9]+$", tokens[3]):
            fmt = [PRE, PRE, TGT, VULN, VULN, SUF]
        else:
            fmt = [PRE, PRE, TGT, PRE, SUF, SUF]
        return fmt

    # TOK-TOK
    def parse_fmt8(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isupper() or tokens[1].isnumeric() or tokens[1] == "Packed":
            fmt = [FAM, SUF]
        else:
            fmt = [CAT, FAM]
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

    # TOK-TOK.TOK
    def parse_fmt10(self, tokens):
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
    def parse_fmt11(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[2].isnumeric():
            fmt = [FAM, FAM, UNK]
        elif tokens[2].islower():
            fmt = [PRE, PRE, SUF]
        else:
            fmt = [UNK, UNK, SUF] # Bad format
        return fmt

    # TOK
    def parse_fmt12(self, tokens):
        return [FAM]

    # TOK.TOK.TOK
    def parse_fmt13(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower():
            if tokens[0].isupper() or len(tokens[0]) <= 3:
                fmt = [UNK, SUF, SUF] # Bad format
            else:
                fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt
        
    # TOK/TOK.TOK.TOK
    def parse_fmt14(self, tokens):
        if tokens[2].islower():
            if tokens[1].isupper():
                fmt = [CAT, UNK, SUF, SUF] # Bad format, usually SUF
            else:
                fmt = [CAT, FAM, SUF, SUF]
        else:
            fmt = [PRE, UNK, UNK, SUF] # Rare bad format
        return fmt

    # TOK/TOK-TOK.TOK
    def parse_fmt15(self, tokens):
        fmt = [TGT, CAT, UNK, SUF]
        if tokens[2].islower():
            fmt = [TGT, CAT, SUF, SUF]
        elif tokens[2].isupper() and not any([c.isdigit() for c in tokens[2]]):
            fmt = [TGT, CAT, SUF, SUF]
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK/TOK
    def parse_fmt16(self, tokens):
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [TGT, SUF]
        elif tokens[1].isupper() or tokens[1].islower():
            fmt = [TGT, UNK] # Bad format
        else:
            fmt = [TGT, FAM]
        return fmt

    # TOK.TOK.TOK.TOK.TOK!TOK
    def parse_fmt17(self, tokens):
        fmt = [PRE, PRE, TGT, UNK, SUF, SUF]
        if tokens[3].isupper():
            fmt = [PRE, PRE, TGT, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, TGT, PRE, SUF, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt18(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower() or tokens[1].isupper():
            fmt = [FAM, SUF]
        else:
            fmt = [UNK, UNK] # Bad format
        return fmt

    # TOK.TOK!TOK
    def parse_fmt19(self, tokens):
        return self.parse_fmt18(tokens) + [SUF]
