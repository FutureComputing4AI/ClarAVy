import re
from claravy.taxonomy import *


class Parse_Mcafeegwedition: # Mcafee, Mcafeegwedition both part of Mcafee

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK!TOK": self.parse_delim_fmt3,
            "TOK/TOK.TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK-TOK!TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt7,
            "TOK-TOK": self.parse_delim_fmt8,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt9,
            "TOK-TOK.TOK": self.parse_delim_fmt10,
            "TOK TOK.TOK": self.parse_delim_fmt11,
            "TOK": self.parse_delim_fmt12,
            "TOK.TOK.TOK": self.parse_delim_fmt13,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt14,
            "TOK/TOK-TOK.TOK": self.parse_delim_fmt15,
            "TOK/TOK": self.parse_delim_fmt16,
            "TOK.TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt17,
            "TOK.TOK": self.parse_delim_fmt18,
            "TOK.TOK!TOK": self.parse_delim_fmt19,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric():
            if len(tokens[2]) <= 2 or tokens[2].isnumeric() or tokens[2] == "Patched":
                tax = [PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        elif tokens[2].islower() or tokens[2].isnumeric():
            if tokens[1].islower():
                tax = [FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper(): # Bad format
            tax = [PRE, PRE, UNK, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, FILE, FAM, SUF] # Very few (if any) actual families in FAM

    # TOK!TOK
    def parse_delim_fmt3(self, tokens):
        return [FAM, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK, SUF]
        if len(tokens[1]) == 1:
            tax = [PRE, SUF, SUF]
        else:
            tax = [FILE, FAM, SUF]
        return tax

    # TOK/TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK-TOK!TOK
    def parse_delim_fmt6(self, tokens):
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

    # TOK.TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, PRE, FILE, UNK, UNK, SUF]
        if re.match("^[M][Ss][0-9]+$", tokens[3]):
            tax = [PRE, PRE, FILE, VULN, VULN, SUF]
        else:
            tax = [PRE, PRE, FILE, PRE, SUF, SUF]
        return tax

    # TOK-TOK
    def parse_delim_fmt8(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isupper() or tokens[1].isnumeric() or tokens[1] == "Packed":
            tax = [FAM, SUF]
        else:
            tax = [CAT, FAM]
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

    # TOK-TOK.TOK
    def parse_delim_fmt10(self, tokens):
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
    def parse_delim_fmt11(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[2].isnumeric():
            tax = [FAM, FAM, UNK]
        elif tokens[2].islower():
            tax = [PRE, PRE, SUF]
        else:
            tax = [UNK, UNK, SUF] # Bad format
        return tax

    # TOK
    def parse_delim_fmt12(self, tokens):
        return [FAM]

    # TOK.TOK.TOK
    def parse_delim_fmt13(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower():
            if tokens[0].isupper() or len(tokens[0]) <= 3:
                tax = [UNK, SUF, SUF] # Bad format
            else:
                tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax
        
    # TOK/TOK.TOK.TOK
    def parse_delim_fmt14(self, tokens):
        if tokens[2].islower():
            if tokens[1].isupper():
                tax = [CAT, UNK, SUF, SUF] # Bad format, usually SUF
            else:
                tax = [CAT, FAM, SUF, SUF]
        else:
            tax = [PRE, UNK, UNK, SUF] # Rare bad format
        return tax

    # TOK/TOK-TOK.TOK
    def parse_delim_fmt15(self, tokens):
        tax = [FILE, CAT, UNK, SUF]
        if tokens[2].islower():
            tax = [FILE, CAT, SUF, SUF]
        elif tokens[2].isupper() and not any([c.isdigit() for c in tokens[2]]):
            tax = [FILE, CAT, SUF, SUF]
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK/TOK
    def parse_delim_fmt16(self, tokens):
        if len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [FILE, SUF]
        elif tokens[1].isupper() or tokens[1].islower():
            tax = [FILE, UNK] # Bad format
        else:
            tax = [FILE, FAM]
        return tax

    # TOK.TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt17(self, tokens):
        tax = [PRE, PRE, FILE, UNK, SUF, SUF]
        if tokens[3].isupper():
            tax = [PRE, PRE, FILE, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, FILE, PRE, SUF, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt18(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower() or tokens[1].isupper():
            tax = [FAM, SUF]
        else:
            tax = [UNK, UNK] # Bad format
        return tax

    # TOK.TOK!TOK
    def parse_delim_fmt19(self, tokens):
        return self.parse_delim_fmt18(tokens) + [SUF]
