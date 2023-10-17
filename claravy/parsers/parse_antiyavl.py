from claravy.taxonomy import *


class Parse_Antiyavl:

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK.TOK": self.parse_fmt1,
            "TOK[TOK]/TOK.TOK.TOK": self.parse_fmt2,
            "TOK[TOK]/TOK.TOK": self.parse_fmt3,
            "TOK/TOK.TOK": self.parse_fmt4,
            "TOK[TOK:TOK-TOK-TOK]/TOK.TOK.TOK": self.parse_fmt5,
            "TOK[TOK:TOK-TOK-TOK]/TOK.TOK": self.parse_fmt6,
            "TOK[:TOK]/TOK.TOK": self.parse_fmt7,
            "TOK[TOK]/TOK.TOK-TOK-TOK": self.parse_fmt8,
            "TOK[TOK:TOK-TOK-TOK,TOK]/TOK.TOK": self.parse_fmt9,
            "TOK[:TOK-TOK-TOK]/TOK.TOK.TOK": self.parse_fmt10,
            "TOK/TOK.TOK.TOK[TOK]": self.parse_fmt11,
            "TOK[TOK-TOK]/TOK.TOK": self.parse_fmt12,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt13,
            "TOK[TOK]/TOK.TOK.TOK.TOK": self.parse_fmt14,
            "TOK[TOK:TOK]/TOK.TOK": self.parse_fmt15,
        }

    # TOK/TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [CAT, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[2].islower():
                fmt = [PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, SUF, SUF]
        else:
            fmt = [CAT, PRE, FAM, SUF]
        return fmt

    # TOK[TOK]/TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        return [CAT, CAT, PRE, FAM, SUF]

    # TOK[TOK]/TOK.TOK
    def parse_fmt3(self, tokens):
        return [CAT, CAT, PRE, FAM]

    # TOK/TOK.TOK
    def parse_fmt4(self, tokens):
        return [CAT, PRE, FAM]

    # TOK[TOK:TOK-TOK-TOK]/TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        return [CAT, CAT, PRE, PRE, PRE, TGT, FAM, SUF]

    # TOK[TOK:TOK-TOK-TOK]/TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [CAT, CAT, PRE, PRE, PRE, UNK, UNK]
        if tokens[6].islower():
            fmt = [CAT, CAT, PRE, PRE, PRE, FAM, SUF]
        else:
            fmt = [CAT, CAT, PRE, PRE, PRE, TGT, FAM]
        return fmt

    # TOK[:TOK]/TOK.TOK
    def parse_fmt7(self, tokens):
        return [CAT, PRE, PRE, SUF]

    # TOK[TOK]/TOK.TOK-TOK-TOK
    def parse_fmt8(self, tokens):
        return [CAT, PRE, PRE, VULN, VULN, VULN]

    # TOK[TOK:TOK-TOK-TOK,TOK]/TOK.TOK
    def parse_fmt9(self, tokens):
        return [CAT, CAT, PRE, PRE, PRE, PRE, TGT, FAM]

    # TOK[:TOK-TOK-TOK]/TOK.TOK.TO]
    def parse_fmt10(self, tokens):
        return [CAT, PRE, PRE, PRE, TGT, FAM, SUF]

    # TOK/TOK.TOK.TOK[TOK]
    def parse_fmt11(self, tokens):
        return [CAT, TGT, FAM, SUF, CAT, NULL]

    # TOK[TOK-TOK]/TOK.TOK
    def parse_fmt12(self, tokens):
        return [CAT, CAT, CAT, TGT, FAM]

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt13(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, SUF]
        if len(tokens[3]) <= 2 and tokens[3].islower():
            fmt = [CAT, TGT, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, PRE, FAM, SUF]
        return fmt

    # TOK[TOK]/TOK.TOK.TOK.TOK
    def parse_fmt14(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, SUF]

    # TOK[TOK:TOK]/TOK.TOK
    def parse_fmt15(self, tokens):
        return [CAT, CAT, PRE, TGT, FAM]
