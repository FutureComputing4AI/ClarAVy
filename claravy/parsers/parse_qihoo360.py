import re
from claravy.taxonomy import *


class Parse_Qihoo360: # Previously used Bitdefender and Antivir/Avira engines

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_fmt2,
            "TOK/TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK.TOK": self.parse_fmt7,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, UNK, SUF]
        if tokens[1].isnumeric():
            fmt = [SUF, SUF, PRE, SUF] # QVM detections
        elif re.match(r"^[Gg]en[0-9]*$", tokens[2]):
            fmt = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, PRE, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        if re.match(r"^QVM[0-9]*$", tokens[2]):
            fmt = [PRE, PRE, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [TGT, CAT, SUF, SUF]
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK/TOK.TOK
    def parse_fmt3(self, tokens):
        return [TGT, CAT, SUF]

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        if re.match(r"^QVM[0-9]*$", tokens[1]):
            fmt = [PRE, PRE, SUF]
        elif tokens[1] in ["cve", "exp"] and tokens[2].isnumeric():
            fmt = [PRE, PRE, VULN]
        elif tokens[2].lower() == "gen":
            fmt = [PRE, PRE, SUF]
        elif len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        if re.match(r"^QVM[0-9]*$", tokens[1]):
            fmt = [PRE, PRE, SUF, PRE, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        if tokens[2].lower() == "cve" and tokens[3].isnumeric and tokens[4].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, VULN]
        elif tokens[3].islower():
            fmt = [PRE, PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt7(self, tokens):
        return [PRE, PRE]
