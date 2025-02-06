import re
from claravy.taxonomy import *


class Parse_Emsisoft: # Bitdefender engine, but extra (TOK) at end. Partnership with Bitdefender.

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK (TOK)": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK (TOK)": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt4,
            "TOK.TOK (TOK)": self.parse_delim_fmt5,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt6,
            "TOK-TOK.TOK.TOK!TOK": self.parse_delim_fmt7,
            "TOK.TOK!TOK": self.parse_delim_fmt8,
            "TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt9,
            "TOK:TOK.TOK.TOK@TOK (TOK)": self.parse_delim_fmt10,
            "TOK:TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_delim_fmt11,
            "TOK:TOK.TOK.TOK.TOK@TOK (TOK)": self.parse_delim_fmt12,
            "TOK.TOK.TOK!.TOK (TOK)": self.parse_delim_fmt13,
        }

    # TOK.TOK.TOK (TOK)
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, SUF, SUF, NULL]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF, SUF, NULL]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF, SUF, NULL]
        elif tokens[2].isupper() or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, NULL]
        elif tokens[2] in ["Gen", "Dam"]:
            tax = [PRE, FAM, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, FAM, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, NULL]
        elif tokens[2] == "Gen" or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, SUF, NULL]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF, SUF, NULL]
        elif len(tokens[2]) <= 3 and tokens[2].isupper() and not tokens[2].startswith("VB"):
            tax = [PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK.TOK (TOK)
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF, NULL]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, NULL]
        elif tokens[2] == "Heur":
            tax = [PRE, PRE, PRE, SUF, SUF, NULL]
        elif tokens[2].isupper():
            tax = [PRE, PRE, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt4(self, tokens): 
        tax = [PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF, NULL]
        elif tokens[2] == "JS":
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric() or re.match(r"^[A-Z0-9]+$", tokens[3]) or tokens[3] == "Gen":
            if tokens[3] == "VB":
                tax = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        elif tokens[1] == "Generic" and tokens[2] == "Malware":
            tax = [PRE, PRE, PRE, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK (TOK)
    def parse_delim_fmt5(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric() or re.match(r"^D[0-9A-Z]+$", tokens[1]):
            tax = [FAM, SUF, SUF, NULL]
        elif tokens[0] == "Application" and tokens[1].isupper():
            tax = [PRE, SUF, SUF, NULL]
        else:
            tax = [PRE, FAM, SUF, NULL]
        return tax

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF, SUF]
        elif tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif re.match(r"Gen[0-9]*", tokens[2]):
            tax = [PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK-TOK.TOK.TOK!TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK.TOK!TOK
    def parse_delim_fmt8(self, tokens):
        tax = [PRE, UNK, SUF]
        if re.match(r"^CVE[0-9]+$", tokens[1]):
            tax = [PRE, VULN, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt9(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF, SUF, NULL]
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            if tokens[2] == "Based":
                tax = [PRE, UNK, UNK, SUF, SUF, SUF, NULL] # Bad format
            elif tokens[2].isnumeric():
                tax = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            if tokens[2].isnumeric():
                tax = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt10(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_delim_fmt11(self, tokens):
        tax = [PRE, PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[4] == "Gen" or tokens[4].isnumeric() or (len(tokens[4]) <= 2 and tokens[4] != "VB"):
            if tokens[3].isnumeric() or len(tokens[3]) <= 2:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK (TOK)
    def parse_delim_fmt12(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF, SUF, SUF, NULL]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF, SUF, NULL]
        elif tokens[3].isupper():
            tax = [PRE, PRE, PRE, SUF, SUF, SUF, SUF, NULL]
        elif tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK!.TOK (TOK)
    def parse_delim_fmt13(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, NULL]
