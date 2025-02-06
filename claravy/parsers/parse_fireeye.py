import re
from claravy.taxonomy import *


class Parse_Fireeye: # Uses Bitdefender engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[0] == "Generic":
            tax = [PRE, SUF, SUF]
        elif tokens[1].isnumeric() or tokens[1].islower():
            tax = [FAM, SUF, SUF]
        elif tokens[1].lower() == "mg":
            tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK, UNK, UNK]
        if "Exploit" in tokens: # Very inconsistent format
            tax = [UNK, UNK, UNK, UNK]
        elif tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Generic" and tokens[2].isupper():
            tax = [PRE, PRE, SUF, SUF]

        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, UNK, FAM, SUF]
        if tokens[0] == "Gen":
            tax = [PRE, PRE, FAM, SUF]
        else:
            tax = [FILE, CAT, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK, CAT, FAM, SUF]
        if tokens[0] == "Gen":
            tax = [PRE, PRE, CAT, FAM, SUF]
        else:
            tax = [CAT, PRE, CAT, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[3].isnumeric() or len(tokens[3]) == 1 or tokens[3] == "Gen":
            if tokens[2].isnumeric():
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, UNK, UNK, UNK, SUF] # No clear format
        return tax

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, PRE, UNK, UNK, UNK, SUF]
        if re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, UNK, SUF]
        elif re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, SUF]
        return tax
