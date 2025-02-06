import re
from claravy.taxonomy import *


class Parse_Qihoo360: # Previously used Bitdefender and Antivir/Avira engines

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK.TOK": self.parse_delim_fmt7,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, UNK, SUF]
        if tokens[1].isnumeric():
            tax = [SUF, SUF, PRE, SUF] # QVM detections
        elif re.match(r"^[Gg]en[0-9]*$", tokens[2]):
            tax = [PRE, PRE, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, PRE, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        if re.match(r"^QVM[0-9]*$", tokens[2]):
            tax = [PRE, PRE, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [FILE, CAT, SUF, SUF]
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK/TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [FILE, CAT, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if re.match(r"^QVM[0-9]*$", tokens[1]):
            tax = [PRE, PRE, SUF]
        elif tokens[1] in ["cve", "exp"] and tokens[2].isnumeric():
            tax = [PRE, PRE, VULN]
        elif tokens[2].lower() == "gen":
            tax = [PRE, PRE, SUF]
        elif len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF]
        elif tokens[2].isupper():
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        if re.match(r"^QVM[0-9]*$", tokens[1]):
            tax = [PRE, PRE, SUF, PRE, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        if tokens[2].lower() == "cve" and tokens[3].isnumeric and tokens[4].isnumeric():
            tax = [PRE, PRE, VULN, VULN, VULN]
        elif tokens[3].islower():
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [PRE, PRE]
