import re
from claravy.taxonomy import *


class Parse_Adaware: # Uses Bitdefender engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK.TOK.TOK@TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK!.TOK": self.parse_delim_fmt8,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt9,
            "TOK.TOK.TOK@TOK": self.parse_delim_fmt10,
            "TOK.TOK": self.parse_delim_fmt11,
            "TOK.TOK-TOK.TOK": self.parse_delim_fmt12,
            "TOK.TOK.TOK!TOK!TOK.TOK": self.parse_delim_fmt13,
            "TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt14,
            "TOK:TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt15,
            "TOK.TOK-TOK-TOK.TOK": self.parse_delim_fmt16,
            "TOK:TOK.TOK.TOK@TOK!TOK": self.parse_delim_fmt17,
            "TOK:TOK.TOK.TOK@TOK@TOK": self.parse_delim_fmt18,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        if tokens[3].isnumeric() and tokens[2].startswith("b"):
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen" or tokens[2].isnumeric() or len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[1].isupper():
                tax = [PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF]
        elif tokens[3] == "Gen" or tokens[3].isnumeric() or tokens[3].isupper():
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, PRE, PRE, UNK, UNK, SUF]
        if tokens[4] == "Gen" or tokens[4].isnumeric() or (len(tokens[4]) <= 2 and tokens[4] != "VB"):
            if tokens[3].isnumeric() or len(tokens[3]) <= 2:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK@TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK!.TOK
    def parse_delim_fmt8(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt9(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif tokens[3].isupper():
            tax = [PRE, PRE, PRE, SUF, SUF, SUF]
        elif tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK@TOK
    def parse_delim_fmt10(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK.TOK
    def parse_delim_fmt11(self, tokens):
        tax = [UNK, UNK]
        if len(tokens[1]) == 4 and tokens[1].isupper():
            tax = [PRE, SUF]
        elif len(tokens[1]) <= 2 or tokens[1].isnumeric() or tokens[1] == "Gen":
            if tokens[0].isupper():
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif len(tokens[1]) == 3 and tokens[1].isupper():
            tax = [PRE, UNK]
        elif re.match(r"^[0-9A-Z]+$", tokens[1]):
            tax = [PRE, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK-TOK.TOK
    def parse_delim_fmt12(self, tokens):
        # TODO: Lots of unusual formats in here
        return [UNK, UNK, UNK, SUF]

    # TOK.TOK.TOK!TOK!TOK.TOK
    def parse_delim_fmt13(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt14(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt15(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK-TOK-TOK.TOK
    def parse_delim_fmt16(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "CVE" and tokens[2].isnumeric() and tokens[3].isnumeric():
            tax = [PRE, VULN, VULN, VULN, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, SUF]
        return tax

    # TOK:TOK.TOK.TOK@TOK!TOK
    def parse_delim_fmt17(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK@TOK@TOK
    def parse_delim_fmt18(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF]
