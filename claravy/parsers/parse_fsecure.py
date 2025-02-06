import re
from claravy.taxonomy import *


class Parse_Fsecure: # Very similar to bitdefender engine. May use Commtouch/Cyren engine. Partnership with Avira.

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK/TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK/TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK:TOK/TOK.TOK": self.parse_delim_fmt7,
            "TOK:TOK/TOK.TOK!TOK": self.parse_delim_fmt8,
            "TOK-TOK:TOK/TOK.TOK!TOK": self.parse_delim_fmt9,
            "TOK:TOK/TOK": self.parse_delim_fmt10,
            "TOK-TOK:TOK/TOK.TOK": self.parse_delim_fmt11,
            "TOK:TOK.TOK.TOK@TOK": self.parse_delim_fmt12,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt13,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt14,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK/TOK.TOK
    def parse_delim_fmt2(self, tokens):    
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic":
            tax = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Generic" and tokens[1] == "Malware":
            tax = [PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK/TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3].isnumeric() or tokens[3].islower():
            tax = [PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[3].isupper():
            tax = [PRE, PRE, PRE, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        if tokens[1] == "Packer":
            if len(tokens[3]) == 1:
                tax = [PRE, PRE, PACK, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, PACK, SUF]
        if tokens[2] == "Generic":
            tax = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[2] == "Malware":
            tax = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            tax = [PRE, CAT, FAM, SUF, SUF]
        elif tokens[3].isupper() and tokens[3] != "VB":
            tax = [PRE, CAT, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK/TOK.TOK
    def parse_delim_fmt7(self, tokens):
        tax = [CAT, FILE, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF]
        return tax

    # TOK:TOK/TOK.TOK!TOK
    def parse_delim_fmt8(self, tokens):
        if re.match(r"^CVE[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF, SUF]
        return tax

    # TOK-TOK:TOK/TOK.TOK!TOK
    def parse_delim_fmt9(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF, SUF]

    # TOK:TOK/TOK
    def parse_delim_fmt10(self, tokens):
        return [CAT, FILE, FAM]

    # TOK-TOK:TOK/TOK.TOK
    def parse_delim_fmt11(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK:TOK.TOK.TOK@TOK
    def parse_delim_fmt12(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF] # tokens[2] never seems to be a family name

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt13(self, tokens):
        tax = [UNK, UNK, UNK, UNK, SUF]
        if tokens[2].isnumeric():
            tax = [FAM, FAM, SUF, SUF, SUF]
        else:
            tax = [CAT, CAT, FILE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt14(self, tokens):
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
