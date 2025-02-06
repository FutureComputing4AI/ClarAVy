import re
from claravy.taxonomy import *


class Parse_Bitdefender:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK.TOK.TOK@TOK": self.parse_delim_fmt6,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF]
        elif any(filter(str.islower, tokens[2])):
            if tokens[1].startswith("Heur"):
                tax = [PRE, PRE, SUF]
            elif tokens[2] in ["Gen", "Dam", "based", "Generic"]:
                if tokens[2] in ["based", "Generic"] or tokens[1].isnumeric():
                    tax = [UNK, SUF, SUF]
                else:
                    tax = [PRE, FAM, SUF]
            elif any(filter(str.isnumeric, tokens[2])):
                tax = [PRE, UNK, SUF]
            else:
                tax = [PRE, CAT, FAM]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [NULL, NULL, NULL, NULL]
        if tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[3].isnumeric():
            if tokens[2] in ["Gen", "GenericKD"] or len(tokens[2]) <= 2:
                tax = [PRE, FAM, SUF, SUF]
            elif tokens[2].isupper() and len(tokens[2]) <= 3:
                tax = [PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        else:
            if len(tokens[2]) <= 3 and tokens[2] != "VB":
                tax = [PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer" and tokens[2] != "Generic":
            tax = [PRE, PRE, PACK, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF]
        elif tokens[2] == "JS":
            tax = [PRE, PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric() or re.match(r"^[A-Z0-9]+$", tokens[3]) or tokens[3] == "Gen":
            if tokens[3] == "VB":
                tax = [PRE, PRE, PRE, FAM, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic" and tokens[2] == "Malware":
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[4].isnumeric() or len(tokens[4]) == 1:
            if tokens[3].isnumeric() or len(tokens[3]) == 1:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if (tokens[4].isupper() and tokens[4] != "VB") or tokens[4] == "Gen":
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK@TOK
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, PRE, UNK, SUF, SUF]
        if tokens[2].startswith("Heur"):
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt7(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif tokens[3].isupper():
            tax = [PRE, PRE, PRE, SUF, SUF, SUF]
        elif tokens[3].isnumeric():
            tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if re.match(r"^M[Ss][0-9]+$", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax


