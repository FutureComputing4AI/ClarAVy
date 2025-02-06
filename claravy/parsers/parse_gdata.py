import re
from claravy.taxonomy import *


class Parse_Gdata: # Uses Bitdefender and in-house engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK-TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK-TOK ": self.parse_delim_fmt6,
            "TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt7,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
            "TOK:TOK.TOK.TOK@TOK": self.parse_delim_fmt9,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt10,
            "TOK:TOK-TOK": self.parse_delim_fmt11,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt12,
            "TOK.TOK-TOK.TOK.TOK@TOK": self.parse_delim_fmt13,
            "TOK.TOK.TOK!.TOK": self.parse_delim_fmt14,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic":
            tax = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric() or len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Generic" and tokens[1] == "Malware":
            tax = [PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if tokens[1] == "Packer":
            if len(tokens[3]) == 1:
                tax = [PRE, PRE, PACK, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, PACK, SUF]
        if tokens[2] == "Generic":
            tax = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[2] == "Malware":
            tax = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            tax = [PRE, CAT, FAM, SUF, SUF]
        elif tokens[3].isupper() and tokens[3] != "VB":
            tax = [PRE, CAT, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK-TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, CAT, CAT, FAM, SUF]

    # TOK:TOK-TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, FAM, SUF, NULL]

    # TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, PRE, UNK, SUF, SUF]
        if tokens[2] == "Heur":
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[4].isnumeric() or len(tokens[4]) == 1:
            if tokens[3].isnumeric() or len(tokens[3]) == 1:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if (tokens[4].isupper() and tokens[4] != "VB") or tokens[4] == "Gen":
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK@TOK
    def parse_delim_fmt9(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt10(self, tokens):
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

    # TOK:TOK-TOK
    def parse_delim_fmt11(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt12(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if re.match(r"^M[Ss][0-9]+$", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK-TOK.TOK.TOK@TOK
    def parse_delim_fmt13(self, tokens):
        return [FILE, CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!.TOK
    def parse_delim_fmt14(self, tokens):
        return [PRE, PRE, SUF, SUF]
