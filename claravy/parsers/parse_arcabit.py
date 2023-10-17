import re
from claravy.taxonomy import *


class Parse_Arcabit: # Uses own engine + Bitdefender engine
 
    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK.TOK.TOK!.TOK": self.parse_fmt6,
            "TOK.TOK": self.parse_fmt7,
            "TOK.TOK.TOK!TOK.TOK": self.parse_fmt8,
            "TOK.TOK.TOK!TOK!TOK.TOK": self.parse_fmt9,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt10,
            "TOK.TOK-TOK-TOK.TOK": self.parse_fmt11,
            "TOK.TOK.TOK-TOK-TOK.TOK": self.parse_fmt12,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF]
        elif any(filter(str.islower, tokens[2])):
            if tokens[1].startswith("Heur"):
                fmt = [PRE, PRE, SUF]
            elif tokens[2] in ["Gen", "Dam", "based", "Generic"]:
                if tokens[2] in ["based", "Generic"] or tokens[1].isnumeric():
                    fmt = [UNK, SUF, SUF]
                else:
                    fmt = [PRE, FAM, SUF]
            elif any(filter(str.isnumeric, tokens[2])):
                fmt = [PRE, UNK, SUF]
            else:
                fmt = [PRE, CAT, FAM]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen" or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 and tokens[2].isupper() and not tokens[2].startswith("VB"):
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer" and tokens[2] != "Generic":
            fmt = [PRE, PRE, PACK, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF]
        elif tokens[2] == "JS":
            fmt = [PRE, PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric() or re.match(r"^[A-Z0-9]+$", tokens[3]) or tokens[3] == "Gen":
            if tokens[3] == "VB":
                fmt = [PRE, PRE, PRE, FAM, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic" and tokens[2] == "Malware":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[3] == "Gen" or len(tokens[3]) <= 2 or tokens[3].isnumeric():
            if tokens[2] == "Gen" or len(tokens[2]) <= 2 or tokens[2].isnumeric():
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK!.TOK
    def parse_fmt6(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0] == "Application": # Typically ends in suffix, bad format
            fmt = [PRE, UNK]
        elif tokens[1].isnumeric() or re.match(r"^D[0-9A-Z]+$", tokens[1]):
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK.TOK!TOK.TOK
    def parse_fmt8(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK!TOK.TOK
    def parse_fmt9(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt10(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, UNK, SUF]
        if re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        elif tokens[4] in ["Gen", "Dam"] or tokens[4].isnumeric() or re.match("^[A-Z0-9]+$", tokens[4]):
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif tokens[3] == "OSX":
            fmt = [PRE, PRE, TGT, TGT, FAM, SUF]
        elif tokens[4] == "Damaged":
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        else: # Bad format
            fmt = [PRE, PRE, UNK, UNK, UNK, SUF]
        return fmt

    # TOK.TOK-TOK-TOK.TOK
    def parse_fmt11(self, tokens):
        return [PRE, VULN, VULN, VULN, SUF]

    # TOK.TOK.TOK-TOK-TOK.TOK
    def parse_fmt12(self, tokens):
        return [PRE, PRE, VULN, VULN, VULN, SUF]
