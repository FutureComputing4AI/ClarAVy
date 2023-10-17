import re
from claravy.taxonomy import *


class Parse_Emsisoft: # Bitdefender engine, but extra (TOK) at end. Partnership with Bitdefender.

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK (TOK)": self.parse_fmt1,
            "TOK.TOK.TOK.TOK (TOK)": self.parse_fmt2,
            "TOK:TOK.TOK.TOK (TOK)": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK (TOK)": self.parse_fmt4,
            "TOK.TOK (TOK)": self.parse_fmt5,
            "TOK.TOK.TOK!TOK": self.parse_fmt6,
            "TOK-TOK.TOK.TOK!TOK": self.parse_fmt7,
            "TOK.TOK!TOK": self.parse_fmt8,
            "TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_fmt9,
            "TOK:TOK.TOK.TOK@TOK (TOK)": self.parse_fmt10,
            "TOK:TOK.TOK.TOK.TOK.TOK (TOK)": self.parse_fmt11,
            "TOK:TOK.TOK.TOK.TOK@TOK (TOK)": self.parse_fmt12,
            "TOK.TOK.TOK!.TOK (TOK)": self.parse_fmt13,
        }

    # TOK.TOK.TOK (TOK)
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, SUF, SUF, NULL]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF, SUF, NULL]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF, SUF, NULL]
        elif tokens[2].isupper() or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, NULL]
        elif tokens[2] in ["Gen", "Dam"]:
            fmt = [PRE, FAM, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, FAM, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK (TOK)
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, NULL]
        elif tokens[2] == "Gen" or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF, NULL]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF, SUF, NULL]
        elif len(tokens[2]) <= 3 and tokens[2].isupper() and not tokens[2].startswith("VB"):
            fmt = [PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK.TOK (TOK)
    def parse_fmt3(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF, NULL]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, NULL]
        elif tokens[2] == "Heur":
            fmt = [PRE, PRE, PRE, SUF, SUF, NULL]
        elif tokens[2].isupper():
            fmt = [PRE, PRE, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK.TOK.TOK (TOK)
    def parse_fmt4(self, tokens): 
        fmt = [PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF, NULL]
        elif tokens[2] == "JS":
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric() or re.match(r"^[A-Z0-9]+$", tokens[3]) or tokens[3] == "Gen":
            if tokens[3] == "VB":
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        elif tokens[1] == "Generic" and tokens[2] == "Malware":
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK (TOK)
    def parse_fmt5(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric() or re.match(r"^D[0-9A-Z]+$", tokens[1]):
            fmt = [FAM, SUF, SUF, NULL]
        elif tokens[0] == "Application" and tokens[1].isupper():
            fmt = [PRE, SUF, SUF, NULL]
        else:
            fmt = [PRE, FAM, SUF, NULL]
        return fmt

    # TOK.TOK.TOK!TOK
    def parse_fmt6(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF, SUF]
        elif tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif re.match(r"Gen[0-9]*", tokens[2]):
            fmt = [PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK-TOK.TOK.TOK!TOK
    def parse_fmt7(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF]

    # TOK.TOK!TOK
    def parse_fmt8(self, tokens):
        fmt = [PRE, UNK, SUF]
        if re.match(r"^CVE[0-9]+$", tokens[1]):
            fmt = [PRE, VULN, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_fmt9(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, SUF, NULL]
        if tokens[3].isnumeric() or tokens[3].islower() or tokens[3] == "Gen":
            if tokens[2] == "Based":
                fmt = [PRE, UNK, UNK, SUF, SUF, SUF, NULL] # Bad format
            elif tokens[2].isnumeric():
                fmt = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            if tokens[2].isnumeric():
                fmt = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_fmt10(self, tokens):
        return [PRE, PRE, FAM, SUF, SUF, SUF, NULL]

    # TOK:TOK.TOK.TOK.TOK.TOK (TOK)
    def parse_fmt11(self, tokens):
        fmt = [PRE, PRE, PRE, UNK, UNK, SUF, SUF, NULL]
        if tokens[4] == "Gen" or tokens[4].isnumeric() or (len(tokens[4]) <= 2 and tokens[4] != "VB"):
            if tokens[3].isnumeric() or len(tokens[3]) <= 2:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK.TOK.TOK@TOK (TOK)
    def parse_fmt12(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, SUF, SUF, NULL]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF, SUF, NULL]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF, SUF, NULL]
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK!.TOK (TOK)
    def parse_fmt13(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, NULL]
