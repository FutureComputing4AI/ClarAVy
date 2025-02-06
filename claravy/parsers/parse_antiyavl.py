from claravy.taxonomy import *


class Parse_Antiyavl:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK[TOK]/TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK[TOK]/TOK.TOK": self.parse_delim_fmt3,
            "TOK/TOK.TOK": self.parse_delim_fmt4,
            "TOK[TOK:TOK-TOK-TOK]/TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK[TOK:TOK-TOK-TOK]/TOK.TOK": self.parse_delim_fmt6,
            "TOK[:TOK]/TOK.TOK": self.parse_delim_fmt7,
            "TOK[TOK]/TOK.TOK-TOK-TOK": self.parse_delim_fmt8,
            "TOK[TOK:TOK-TOK-TOK,TOK]/TOK.TOK": self.parse_delim_fmt9,
            "TOK[:TOK-TOK-TOK]/TOK.TOK.TOK": self.parse_delim_fmt10,
            "TOK/TOK.TOK.TOK[TOK]": self.parse_delim_fmt11,
            "TOK[TOK-TOK]/TOK.TOK": self.parse_delim_fmt12,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt13,
            "TOK[TOK]/TOK.TOK.TOK.TOK": self.parse_delim_fmt14,
            "TOK[TOK:TOK]/TOK.TOK": self.parse_delim_fmt15,
        }

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[2].islower():
                tax = [PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, SUF, SUF]
        else:
            tax = [CAT, PRE, FAM, SUF]
        return tax

    # TOK[TOK]/TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, CAT, PRE, FAM, SUF]

    # TOK[TOK]/TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [CAT, CAT, PRE, FAM]

    # TOK/TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT, PRE, FAM]

    # TOK[TOK:TOK-TOK-TOK]/TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [CAT, CAT, PRE, PRE, PRE, FILE, FAM, SUF]

    # TOK[TOK:TOK-TOK-TOK]/TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [CAT, CAT, PRE, PRE, PRE, UNK, UNK]
        if tokens[6].islower():
            tax = [CAT, CAT, PRE, PRE, PRE, FAM, SUF]
        else:
            tax = [CAT, CAT, PRE, PRE, PRE, FILE, FAM]
        return tax

    # TOK[:TOK]/TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, PRE, PRE, SUF]

    # TOK[TOK]/TOK.TOK-TOK-TOK
    def parse_delim_fmt8(self, tokens):
        return [CAT, PRE, PRE, VULN, VULN, VULN]

    # TOK[TOK:TOK-TOK-TOK,TOK]/TOK.TOK
    def parse_delim_fmt9(self, tokens):
        return [CAT, CAT, PRE, PRE, PRE, PRE, FILE, FAM]

    # TOK[:TOK-TOK-TOK]/TOK.TOK.TO]
    def parse_delim_fmt10(self, tokens):
        return [CAT, PRE, PRE, PRE, FILE, FAM, SUF]

    # TOK/TOK.TOK.TOK[TOK]
    def parse_delim_fmt11(self, tokens):
        return [CAT, FILE, FAM, SUF, CAT, NULL]

    # TOK[TOK-TOK]/TOK.TOK
    def parse_delim_fmt12(self, tokens):
        return [CAT, CAT, CAT, FILE, FAM]

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt13(self, tokens):
        tax = [CAT, FILE, UNK, UNK, SUF]
        if len(tokens[3]) <= 2 and tokens[3].islower():
            tax = [CAT, FILE, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, PRE, FAM, SUF]
        return tax

    # TOK[TOK]/TOK.TOK.TOK.TOK
    def parse_delim_fmt14(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF, SUF]

    # TOK[TOK:TOK]/TOK.TOK
    def parse_delim_fmt15(self, tokens):
        return [CAT, CAT, PRE, FILE, FAM]
