import re
from claravy.taxonomy import *


class Parse_Fsecure: # Very similar to bitdefender engine. May use Commtouch/Cyren engine. Partnership with Avira.

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK/TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK/TOK.TOK.TOK": self.parse_fmt5,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK:TOK/TOK.TOK": self.parse_fmt7,
            "TOK:TOK/TOK.TOK!TOK": self.parse_fmt8,
            "TOK-TOK:TOK/TOK.TOK!TOK": self.parse_fmt9,
            "TOK:TOK/TOK": self.parse_fmt10,
            "TOK-TOK:TOK/TOK.TOK": self.parse_fmt11,
            "TOK:TOK.TOK.TOK@TOK": self.parse_fmt12,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt13,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_fmt14,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK.TOK/TOK.TOK
    def parse_fmt2(self, tokens):    
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic":
            fmt = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Generic" and tokens[1] == "Malware":
            fmt = [PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK/TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3].isnumeric() or tokens[3].islower():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, PRE, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        if tokens[1] == "Packer":
            if len(tokens[3]) == 1:
                fmt = [PRE, PRE, PACK, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, PACK, SUF]
        if tokens[2] == "Generic":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[2] == "Malware":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            fmt = [PRE, CAT, FAM, SUF, SUF]
        elif tokens[3].isupper() and tokens[3] != "VB":
            fmt = [PRE, CAT, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK/TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [CAT, TGT, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF]
        return fmt

    # TOK:TOK/TOK.TOK!TOK
    def parse_fmt8(self, tokens):
        if re.match(r"^CVE[0-9]+$", tokens[2]):
            fmt = [CAT, TGT, VULN, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, SUF, SUF]
        return fmt

    # TOK-TOK:TOK/TOK.TOK!TOK
    def parse_fmt9(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF, SUF]

    # TOK:TOK/TOK
    def parse_fmt10(self, tokens):
        return [CAT, TGT, FAM]

    # TOK-TOK:TOK/TOK.TOK
    def parse_fmt11(self, tokens):
        return [CAT, CAT, TGT, FAM, SUF]

    # TOK:TOK.TOK.TOK@TOK
    def parse_fmt12(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF] # tokens[2] never seems to be a family name

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt13(self, tokens):
        fmt = [UNK, UNK, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            fmt = [FAM, FAM, SUF, SUF, SUF]
        else:
            fmt = [CAT, CAT, TGT, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_fmt14(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt
