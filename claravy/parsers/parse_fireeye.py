import re
from claravy.taxonomy import *


class Parse_Fireeye: # Uses Bitdefender engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt5,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[0] == "Generic":
            fmt = [PRE, SUF, SUF]
        elif tokens[1].isnumeric() or tokens[1].islower():
            fmt = [FAM, SUF, SUF]
        elif tokens[1].lower() == "mg":
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK, UNK, UNK]
        if "Exploit" in tokens: # Very inconsistent format
            fmt = [UNK, UNK, UNK, UNK]
        elif tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic" and tokens[2].isupper():
            fmt = [PRE, PRE, SUF, SUF]

        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [UNK, UNK, FAM, SUF]
        if tokens[0] == "Gen":
            fmt = [PRE, PRE, FAM, SUF]
        else:
            fmt = [TGT, CAT, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK, CAT, FAM, SUF]
        if tokens[0] == "Gen":
            fmt = [PRE, PRE, CAT, FAM, SUF]
        else:
            fmt = [CAT, PRE, CAT, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric() or len(tokens[3]) == 1 or tokens[3] == "Gen":
            if tokens[2].isnumeric():
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, UNK, UNK, UNK, SUF] # No clear format
        return fmt

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, UNK, SUF]
        if re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, UNK, SUF]
        elif re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, SUF]
        return fmt
