import re
from claravy.taxonomy import *


class Parse_Alibaba:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK:TOK/TOK-TOK-TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK/TOK_TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK/TOK-TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK:TOK/TOK_TOK_TOK.TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt8,
        }

    # TOK:TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK:TOK/TOK-TOK-TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [CAT, FILE, UNK, UNK, UNK, SUF]
        if tokens[2] in ["CVE", "CAN"]:
            tax = [CAT, FILE, VULN, VULN, VULN, SUF]
        elif tokens[4] == "based" or tokens[4].isnumeric():
            tax = [CAT, FILE, FAM, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, FAM, FAM, SUF]
        return tax

    # TOK:TOK/TOK_TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [CAT, FILE, UNK, UNK, SUF]
        if tokens[4] == "None":
            tax = [CAT, FILE, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "gen" or len(tokens[3]) == 1:
            tax = [CAT, FILE, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, FAM, SUF]
        return tax

    # TOK:TOK/TOK-TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [CAT, FILE, UNK, UNK, SUF]
        if tokens[3] == "based":
            tax = [CAT, FILE, FAM, SUF, SUF]
        elif re.match("MS[0-9]{2}", tokens[2]) or re.match("CVE[0-9]{4}", tokens[2]):
            tax = [CAT, FILE, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "gen":
            tax = [CAT, FILE, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [UNK, UNK, UNK, UNK]
        if len(tokens[0]) == 1 and len(tokens[1]) == 1 and len(tokens[2]) == 3:
            tax = [PRE, PRE, PRE, FAM]
        else:
            tax = [PRE, FILE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]

    # TOK:TOK/TOK_TOK_TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [CAT, FILE, UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric() and tokens[4].isnumeric():
            tax = [CAT, FILE, FAM, SUF, SUF, SUF]
        elif tokens[4].isnumeric():
            tax = [CAT, FILE, FAM, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, FAM, FAM, SUF]
        return tax

    # TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt8(self, tokens):
        return [PRE, FILE, FAM, SUF, SUF]
