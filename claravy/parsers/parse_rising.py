import re
from claravy.taxonomy import *


class Parse_Rising:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK!TOK.TOK (TOK)": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK!TOK.TOK (TOK:TOK:TOK)": self.parse_delim_fmt3,
            "TOK.TOK/TOK!TOK.TOK (TOK)": self.parse_delim_fmt4,
            "TOK.TOK!TOK.TOK (TOK:TOK)": self.parse_delim_fmt5,
            "TOK:TOK.TOK!TOK.TOK": self.parse_delim_fmt6,
            "TOK:TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt8,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt9,
            "TOK.TOK@TOK!TOK.TOK (TOK)": self.parse_delim_fmt10,
            "TOK:TOK.TOK.TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt11,
            "TOK.TOK!TOK": self.parse_delim_fmt12,
            "TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt13,
            "TOK.TOK.TOK.TOK (TOK:TOK)": self.parse_delim_fmt14,
            "TOK.TOK.TOK": self.parse_delim_fmt15,
            "TOK:TOK.TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt16,
            "TOK.TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt17,
            "TOK:TOK.TOK.TOK!TOK": self.parse_delim_fmt18,
            "TOK.TOK-TOK!TOK.TOK (TOK:TOK:TOK)": self.parse_delim_fmt19,
            "TOK:TOK.TOK-TOK/TOK!TOK.TOK": self.parse_delim_fmt20,
            "TOK:TOK.TOK(TOK)!TOK.TOK [TOK]": self.parse_delim_fmt21,
            "TOK:TOK.TOK!TOK.TOK [TOK]": self.parse_delim_fmt22,
            "TOK.TOK@TOK.TOK (TOK:TOK)": self.parse_delim_fmt23,
            "TOK:TOK.TOK@TOK!TOK.TOK": self.parse_delim_fmt24,
            "TOK.TOK.TOK (TOK)": self.parse_delim_fmt25,
            "TOK": self.parse_delim_fmt26,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt27,
            "TOK:TOK.TOK/TOK!TOK.TOK [TOK]": self.parse_delim_fmt28,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt29,
            "TOK.TOK-TOK!TOK.TOK (TOK:TOK)": self.parse_delim_fmt30,
        }

    # TOK.TOK!TOK.TOK (TOK)
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, UNK, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            tax = [CAT, VULN, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, FAM, SUF, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [CAT, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            tax = [CAT, FAM, SUF, SUF]
        else:
            tax = [CAT, PRE, FAM, SUF]
        return tax

    # TOK.TOK!TOK.TOK (TOK:TOK:TOK)
    def parse_delim_fmt3(self, tokens):
        tax = [CAT, UNK, SUF, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            tax = [CAT, VULN, SUF, SUF, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, FAM, SUF, SUF, SUF, SUF, SUF, NULL]
        return tax

    # TOK.TOK/TOK!TOK.TOK (TOK)
    def parse_delim_fmt4(self, tokens):
        if tokens[2].isupper():
            tax = [CAT, FAM, PRE, SUF, SUF, SUF, NULL]
        elif tokens[1].isupper():
            tax = [CAT, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, UNK, UNK, SUF, SUF, SUF, NULL] # Bad format
        return tax

    # TOK.TOK!TOK.TOK (TOK:TOK)
    def parse_delim_fmt5(self, tokens):
        tax = [CAT, UNK, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]):
            tax = [CAT, VULN, SUF, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, FAM, SUF, SUF, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK!TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [FILE, CAT, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, PRE, PRE, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PRE, PACK, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt8(self, tokens):
        tax = [UNK, UNK, UNK, SUF, SUF, NULL]
        if tokens[2].isnumeric():
            if tokens[1].isupper():
                tax = [UNK, UNK, UNK, SUF, SUF, NULL] # Bad format
            else:
                tax = [CAT, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt9(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                tax = [PRE, PRE, UNK, SUF, SUF] # Bad format
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [CAT, PRE, FILE, FAM, SUF]
        return tax

    # TOK.TOK@TOK!TOK.TOK (TOK)
    def parse_delim_fmt10(self, tokens):
        return [PRE, FAM, SUF, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK.TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt11(self, tokens):
        return [FILE, CAT, CAT, PRE, FILE, FAM, SUF, SUF]

    # TOK.TOK!TOK
    def parse_delim_fmt12(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt13(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                tax = [PRE, PRE, UNK, SUF, SUF, SUF, NULL] # Bad format
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, PRE, FILE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK (TOK:TOK)
    def parse_delim_fmt14(self, tokens):
        tax = [CAT, UNK, UNK, SUF, SUF, SUF, NULL]
        if tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
        elif tokens[3].islower() or tokens[3] == "GEN":
            tax = [CAT, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, PRE, PRE, SUF, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt15(self, tokens):
        if tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            if tokens[2].isnumeric() or len(tokens[2]) <= 2:
                tax = [FAM, SUF, SUF]
            else:
                tax = [CAT, PRE, FAM]
        elif tokens[2].islower() or tokens[2] == "GEN" or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax        

    # TOK:TOK.TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt16(self, tokens):
        return [FILE, CAT, PRE, FILE, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt17(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                tax = [PRE, PRE, UNK, SUF, SUF, SUF, SUF, NULL] # Bad format
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, PRE, PRE, FILE, FAM, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK.TOK!TOK
    def parse_delim_fmt18(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3].islower() or tokens[3].isupper() or tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK-TOK!TOK.TOK (TOK:TOK:TOK)
    def parse_delim_fmt19(self, tokens):
        tax = [CAT, UNK, UNK, SUF, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            tax = [CAT, VULN, VULN, SUF, SUF, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, CAT, FAM, SUF, SUF, SUF, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK-TOK/TOK!TOK.TOK
    def parse_delim_fmt20(self, tokens):
        return [FILE, PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK(TOK)!TOK.TOK [TOK]
    def parse_delim_fmt21(self, tokens):
        return [FILE, PRE, PRE, FAM, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK!TOK.TOK [TOK]
    def parse_delim_fmt22(self, tokens):
        return [FILE, CAT, FAM, SUF, SUF, SUF, NULL]

    # TOK.TOK@TOK.TOK (TOK:TOK)
    def parse_delim_fmt23(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK@TOK!TOK.TOK
    def parse_delim_fmt24(self, tokens):
        return [FILE, PRE, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK (TOK)
    def parse_delim_fmt25(self, tokens):
        return self.parse_delim_fmt15(tokens) + [SUF, NULL]

    # TOK
    def parse_delim_fmt26(self, tokens):
        tax = [UNK]
        if tokens[0].isnumeric():
            tax = [SUF]
        else:
            tax = [FAM]
        return tax

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt27(self, tokens):
        if tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isupper() or len(tokens[2]) <= 3:
                tax = [PRE, PRE, UNK, SUF, SUF, SUF] # Bad format
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            tax = [CAT, PRE, PRE, FILE, FAM, SUF]
        return tax

    # TOK:TOK.TOK/TOK!TOK.TOK [TOK]
    def parse_delim_fmt28(self, tokens):
        return [FILE, PRE, FAM, UNK, SUF, SUF, SUF, NULL] # tokens[3] can be PRE, SUF, FILE

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt29(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK-TOK!TOK.TOK (TOK:TOK)
    def parse_delim_fmt30(self, tokens):
        tax = [CAT, UNK, UNK, SUF, SUF, SUF, SUF, NULL]
        if re.match(r"^MS[0-9]+$", tokens[1]) and tokens[2].isnumeric():
            tax = [CAT, VULN, VULN, SUF, SUF, SUF, SUF, NULL]
        else:
            tax = [CAT, CAT, FAM, SUF, SUF, SUF, SUF, NULL]
        return tax
