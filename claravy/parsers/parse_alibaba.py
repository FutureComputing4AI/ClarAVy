import re
from claravy.taxonomy import *


class Parse_Alibaba:

    def __init__(self):
        self.parse_fmt = {
            "TOK:TOK/TOK.TOK": self.parse_fmt1,
            "TOK:TOK/TOK-TOK-TOK.TOK": self.parse_fmt2,
            "TOK:TOK/TOK_TOK.TOK": self.parse_fmt3,
            "TOK:TOK/TOK-TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK:TOK/TOK_TOK_TOK.TOK": self.parse_fmt7,
            "TOK.TOK.TOK-TOK.TOK": self.parse_fmt8,
        }

    # TOK:TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        return [CAT, TGT, FAM, SUF]

    # TOK:TOK/TOK-TOK-TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, UNK, SUF]
        if tokens[2] in ["CVE", "CAN"]:
            fmt = [CAT, TGT, VULN, VULN, VULN, SUF]
        elif tokens[4] == "based" or tokens[4].isnumeric():
            fmt = [CAT, TGT, FAM, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, FAM, FAM, SUF]
        return fmt

    # TOK:TOK/TOK_TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, SUF]
        if tokens[4] == "None":
            fmt = [CAT, TGT, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "gen" or len(tokens[3]) == 1:
            fmt = [CAT, TGT, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, FAM, SUF]
        return fmt

    # TOK:TOK/TOK-TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, SUF]
        if tokens[3] == "based":
            fmt = [CAT, TGT, FAM, SUF, SUF]
        elif re.match("MS[0-9]{2}", tokens[2]) or re.match("CVE[0-9]{4}", tokens[2]):
            fmt = [CAT, TGT, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "gen":
            fmt = [CAT, TGT, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [UNK, UNK, UNK, UNK]
        if len(tokens[0]) == 1 and len(tokens[1]) == 1 and len(tokens[2]) == 3:
            fmt = [PRE, PRE, PRE, FAM]
        else:
            fmt = [PRE, TGT, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]

    # TOK:TOK/TOK_TOK_TOK.TOK
    def parse_fmt7(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric() and tokens[4].isnumeric():
            fmt = [CAT, TGT, FAM, SUF, SUF, SUF]
        elif tokens[4].isnumeric():
            fmt = [CAT, TGT, FAM, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, FAM, FAM, FAM, SUF]
        return fmt

    # TOK.TOK.TOK-TOK.TOK
    def parse_fmt8(self, tokens):
        return [PRE, TGT, FAM, SUF, SUF]
