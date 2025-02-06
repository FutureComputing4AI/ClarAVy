import re
from claravy.taxonomy import *


class Parse_Mcafee: # Mcafee, Mcafeegwedition both part of Mcafee

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK!TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK-TOK": self.parse_delim_fmt3,
            "TOK-TOK!TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK-TOK.TOK": self.parse_delim_fmt6,
            "TOK TOK.TOK": self.parse_delim_fmt7,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt9,
            "TOK/TOK": self.parse_delim_fmt10,
            "TOK": self.parse_delim_fmt11,
            "TOK/TOK-TOK.TOK": self.parse_delim_fmt12,
            "TOK.TOK": self.parse_delim_fmt13,
            "TOK.TOK!TOK": self.parse_delim_fmt14,
            "TOK.TOK.TOK": self.parse_delim_fmt15,
            "TOK-TOK-TOK": self.parse_delim_fmt16,
            "TOK/TOK.TOK.TOK!TOK": self.parse_delim_fmt17,
            "TOK TOK.TOK!TOK": self.parse_delim_fmt18,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt19,
            "TOK TOK!TOK": self.parse_delim_fmt20,
            "TOK!TOK.TOK": self.parse_delim_fmt21,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt22,
            "TOK/TOK-TOK": self.parse_delim_fmt23,
        }

    # TOK!TOK
    def parse_delim_fmt1(self, tokens):
        return [FAM, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            tax = [PRE, SUF, SUF]
        else:
            tax = [UNK, FAM, SUF] # Is tokens[0] CAT or FILE?
        return tax

    # TOK-TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isupper() or tokens[1].isnumeric() or tokens[1] == "Packed":
            tax = [FAM, SUF]
        else:
            tax = [CAT, FAM]
        return tax

    # TOK-TOK!TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK, SUF]
        if re.match(r"^Generic[A-Z]+$", tokens[0]):
            tax = [SUF, SUF, SUF]
        elif tokens[1].isupper():
            tax = [FAM, SUF, SUF]
        elif tokens[1].islower() or tokens[1].isnumeric(): # Bad format
            tax = [UNK, SUF, SUF]
        elif tokens[1] == "Gen":
            tax = [FAM, SUF, SUF]
        else:
            tax = [CAT, FAM, SUF]
        return tax

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK-TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [CAT, UNK, UNK]
        if tokens[2].islower():
            if tokens[1].isupper() and len(tokens[1]) <= 3 and tokens[1] != "VB":
                tax = [CAT, SUF, SUF]
            else:
                tax = [CAT, FAM, SUF]
        else:
            tax = [CAT, UNK, UNK] # Bad format
        return tax

    # TOK TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[2].isnumeric():
            tax = [FAM, FAM, UNK]
        else:
            tax = [UNK, UNK, SUF] # Rarely [FAM, FAM, SUF] but usually [PRE, PRE, SUF]
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [FILE, UNK, UNK, SUF]
        if tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            tax = [FILE, FAM, SUF, SUF]
        else:
            tax = [FILE, PRE, FAM, SUF]
        return tax

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt9(self, tokens):
        if tokens[2].islower():
            if tokens[1].isupper():
                tax = [CAT, UNK, SUF, SUF] # Bad format, usually SUF
            else:
                tax = [CAT, FAM, SUF, SUF]
        else:
            tax = [PRE, UNK, UNK, SUF] # Rare bad format
        return tax

    # TOK/TOK
    def parse_delim_fmt10(self, tokens):
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [FILE, SUF]
        elif tokens[1].isupper() or tokens[1].islower():
            tax = [FILE, UNK] # Bad format
        else:
            tax = [FILE, FAM]
        return tax

    # TOK
    def parse_delim_fmt11(self, tokens):
        return [FAM]

    # TOK/TOK-TOK.TOK
    def parse_delim_fmt12(self, tokens):
        tax = [FILE, CAT, UNK, SUF]
        if tokens[2].islower():
            tax = [FILE, CAT, SUF, SUF]
        elif tokens[2].isupper() and not any([c.isdigit() for c in tokens[2]]):
            tax = [FILE, CAT, SUF, SUF]
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt13(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower() or tokens[1].isupper():
            tax = [FAM, SUF]
        else:
            tax = [UNK, UNK] # Bad format
        return tax

    # TOK.TOK!TOK
    def parse_delim_fmt14(self, tokens):
        return self.parse_delim_fmt13(tokens) + [SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt15(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[1].islower():
            tax = [FAM, SUF, SUF]
        elif tokens[1].isnumeric():
            if tokens[2].islower():
                tax = [FAM, SUF, SUF]
            else:
                tax = [UNK, SUF, UNK] # Bad format
        else:
            tax = [UNK, UNK, SUF] # Bad format
        return tax

    # TOK-TOK-TOK
    def parse_delim_fmt16(self, tokens):
        tax = [UNK, UNK, UNK]
        if re.match(r"^CVE[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN]
        elif re.match(r"^MS[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN]
        elif tokens[1].isupper():
            tax = [PRE, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK.TOK!TOK
    def parse_delim_fmt17(self, tokens):
        return [FILE, FAM, PRE, SUF, SUF]

    # TOK TOK.TOK!TOK
    def parse_delim_fmt18(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt19(self, tokens):
        return [FILE, FAM, UNK, SUF, SUF] # tokens[2] either CAT or SUF

    # TOK TOK!TOK
    def parse_delim_fmt20(self, tokens):
        return [PRE, FAM, SUF]

    # TOK!TOK.TOK
    def parse_delim_fmt21(self, tokens):
        return [FAM, SUF, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt22(self, tokens):
        return self.parse_delim_fmt9(tokens) + [SUF]

    # TOK/TOK-TOK
    def parse_delim_fmt23(self, tokens):
        tax = [FILE, CAT, UNK]
        if tokens[2].islower():
            tax = [FILE, CAT, SUF]
        elif tokens[2].isupper() and not any([c.isdigit() for c in tokens[2]]):
            tax = [FILE, CAT, SUF]
        else:
            tax = [FILE, CAT, FAM]
        return tax

    
