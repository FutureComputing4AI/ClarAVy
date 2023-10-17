from claravy.taxonomy import *


class Parse_Catquickheal:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK": self.parse_fmt4,
            "(TOK) - TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK-TOK.TOK.TOK": self.parse_fmt7,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK/TOK.TOK
    def parse_fmt2(self, tokens):
        return [TGT, FAM, SUF]



    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].islower() or tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2] == "MUE": # Unsure of what this token is, but common
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            fmt = [PRE, UNK, UNK, SUF] # Bad format
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric():
            if tokens[1].isupper():
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [UNK, SUF]
        elif tokens[1].isupper() and not any([c.isdigit() for c in tokens[1]]):
            fmt = [PRE, UNK]
        elif tokens[1].islower():            
            fmt = [UNK, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # (TOK) - TOK
    def parse_fmt5(self, tokens):
        return [NULL, PRE, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, UNK]
        if tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[2] == "CVE" and tokens[3].isnumeric() and tokens[4].isnumeric():
            fmt = [PRE, FAM, VULN, VULN, VULN]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK-TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        if tokens[2].isnumeric():
            fmt = [UNK, UNK, SUF, SUF] # Bad format
        else:
            fmt = [CAT, CAT, FAM, SUF]
        return fmt

