import re
from claravy.taxonomy import *


class Parse_Microworldescan: # Runs on BitDefender engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK.TOK.TOK@TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt7,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt8,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        # Probably not perfect, but unsure if it can be improved. Might be missing some packers.
        tax = [NULL, NULL, NULL]
        if tokens[2].isnumeric():
            tax = [PRE, FAM, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[2]):
            tax = [PRE, FAM, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 or (len(tokens[2]) == 4 and tokens[2].isupper()):
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
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
        elif len(tokens[2]) <= 3 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF]
        elif tokens[3] == "Gen" or tokens[3].isnumeric() or tokens[3].isupper():
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, PRE, PRE, UNK, UNK, SUF]
        if tokens[4] == "Gen" or tokens[4].isnumeric() or (len(tokens[4]) <= 2 and tokens[4] != "VB"):
            if tokens[3].isnumeric() or len(tokens[3]) <= 2:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK@TOK
    def parse_delim_fmt6(self, tokens):
        if tokens[2] == "Heur":
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        if re.match(r"[0-9A-F]{8}", tokens[4]):
            if tokens[3].isnumeric():
                tax = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[3].isupper() and len(tokens[3]) <= 3:
                tax = [PRE, PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF]
        elif tokens[2] == "CVE":
            tax = [PRE, PRE, VULN, VULN, VULN]
        elif re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF]
        elif "plugin" in [tokens[2].lower(), tokens[3].lower(), tokens[4].lower()]:
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            if tokens[2].isnumeric() or tokens[2] in ["Dropper", "Based"]:
                tax = [PRE, FAM, SUF, SUF, SUF]
            elif len(tokens[2]) <= 2 and tokens[2] != "VB":
                tax = [PRE, FAM, SUF, SUF, SUF]
            elif tokens[2] == "Gen":
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].islower():
            tax = [PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[3]) == 2:
            if re.match(r"V[0-9]", tokens[3]):
                tax = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[1].lower() == "aol":
                tax = [PRE, PRE, PRE, SUF, SUF]
            elif tokens[3].lower() == "vb":
                tax = [PRE, PRE, PRE, PRE, SUF]
            elif tokens[2] == "VB":
                tax = [PRE, PRE, FAM, SUF, SUF]
            elif len(tokens[2]) <= 3:
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[4].isnumeric():
            if len(tokens[3]) <= 3:
                if len(tokens[2]) <= 3:
                    tax = [PRE, FAM, SUF, SUF, SUF]
                else:
                    tax = [PRE, PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt8(self, tokens):
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
