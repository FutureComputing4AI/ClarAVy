import re
from claravy.taxonomy import *


class Parse_Vipre: # Avware uses Vipre engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt1,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK (TOK)": self.parse_delim_fmt3,
            "TOK (TOK)": self.parse_delim_fmt4,
            "TOK-TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt6,
            "TOK-TOK.TOK.TOK (TOK)": self.parse_delim_fmt7,
            "TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt8,
            "TOK/TOK (TOK)": self.parse_delim_fmt9,
            "TOK.TOK.TOK.TOK!TOK (TOK)": self.parse_delim_fmt10,
            "TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt11,
            "TOK TOK (TOK)": self.parse_delim_fmt12,
            "TOK.TOK": self.parse_delim_fmt13,
            "TOK.TOK.TOK.TOK (TOK-TOK)": self.parse_delim_fmt14,
            "TOK.TOK.TOK": self.parse_delim_fmt15,
            "TOK.TOK.TOK!TOK (TOK)": self.parse_delim_fmt16,
            "TOK": self.parse_delim_fmt17,
            "TOK TOK. (TOK)": self.parse_delim_fmt18,
            "TOK.TOK.TOK-TOK (TOK)": self.parse_delim_fmt19,
            "TOK.TOK (TOK)": self.parse_delim_fmt20,
        }

    # TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, FILE, UNK, UNK, SUF, NULL]
        if tokens[2] == "Packer":
            tax = [CAT, FILE, PRE, PACK, SUF, NULL]
        else:
            tax = [CAT, FILE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt2(self, tokens):
        if tokens[2] == "Generic":
            tax = [PRE, PRE, PRE, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK (TOK)
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF, NULL]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF, SUF, NULL]
        elif len(tokens[2]) <= 2 or tokens[2].lower() == "gen":
            tax = [PRE, FAM, SUF, SUF, NULL]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, NULL]
        else:
            tax = [PRE, FILE, FAM, SUF, NULL]
        return tax

    # TOK (TOK)
    def parse_delim_fmt4(self, tokens):
        return [FAM, SUF, NULL]

    # TOK-TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt5(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF, SUF, NULL]

    # TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt6(self, tokens):
        tax = [CAT, FILE, UNK, SUF, SUF]
        if tokens[2] == "Generic":
            tax = [CAT, FILE, PRE, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF, SUF]
        return tax

    # TOK-TOK.TOK.TOK (TOK)
    def parse_delim_fmt7(self, tokens):
        tax = [CAT, CAT, UNK, UNK, SUF, NULL]
        if tokens[3].islower():
            tax = [CAT, CAT, FAM, SUF, SUF, NULL]
        elif len(tokens[3]) <= 2 or tokens[3].isupper():
            tax = [CAT, CAT, UNK, SUF, SUF, NULL] # Bad format
        else:
            tax = [CAT, CAT, FILE, FAM, SUF, NULL]
        return tax

    # TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt8(self, tokens):
        if tokens[2] == "Generic":
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK/TOK (TOK)
    def parse_delim_fmt9(self, tokens):
        return [FAM, FAM, SUF, NULL]

    # TOK.TOK.TOK.TOK!TOK (TOK)
    def parse_delim_fmt10(self, tokens):
        return self.parse_delim_fmt6(tokens) + [SUF, NULL]

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt11(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF, SUF, NULL]

    # TOK TOK (TOK)
    def parse_delim_fmt12(self, tokens):
        if tokens[0] == "Corrupted":
            tax = [PRE, PRE, SUF, NULL]
        else:
            tax = [FAM, FAM, SUF, NULL]
        return tax

    # TOK.TOK
    def parse_delim_fmt13(self, tokens):
        if tokens[1].isnumeric() or tokens[1].islower():
            tax = [FAM, SUF]
        else:
            tax = [UNK, FAM] # Some [FAM, FAM] and some [CAT, FAM]
        return tax

    # TOK.TOK.TOK.TOK (TOK-TOK)
    def parse_delim_fmt14(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF, NULL]

    # TOK.TOK.TOK
    def parse_delim_fmt15(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[2] == "gen":
            tax = [PRE, PRE, SUF]
        elif tokens[2].isupper() or tokens[2].islower(): # Bad format
            tax = [PRE, UNK, UNK]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK!TOK (TOK)
    def parse_delim_fmt16(self, tokens):
        tax = [PRE, UNK, UNK, SUF, SUF, SUF]
        if len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        return tax

    # TOK
    def parse_delim_fmt17(self, tokens):
        return [FAM]

    # TOK TOK. (TOK)
    def parse_delim_fmt18(self, tokens):
        return [FAM, FAM, SUF, NULL]

    # TOK.TOK.TOK-TOK (TOK)
    def parse_delim_fmt19(self, tokens):
        tax = []
        if re.match(r"^CVE[0-9]{4}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF, NULL]
        elif tokens[2].islower() or len(tokens[2]) <= 2:
            tax = [PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, FILE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK (TOK)
    def parse_delim_fmt20(self, tokens):
        tax = [UNK, UNK, SUF, NULL]
        if tokens[1].islower() or len(tokens[1]) == 1 or tokens[1] == "Gen":
            tax = [FAM, SUF, SUF, NULL]
        else:
            tax = [PRE, FAM, SUF, SUF]
        return tax
