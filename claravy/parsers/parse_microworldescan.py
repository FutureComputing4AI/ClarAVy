import re
from claravy.taxonomy import *


class Parse_Microworldescan: # Runs on BitDefender engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_fmt5,
            "TOK:TOK.TOK.TOK@TOK": self.parse_fmt6,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt7,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_fmt8,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        # Probably not perfect, but unsure if it can be improved. Might be missing some packers.
        fmt = [NULL, NULL, NULL]
        if tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[2]):
            fmt = [PRE, FAM, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 or (len(tokens[2]) == 4 and tokens[2].isupper()):
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [NULL, NULL, NULL, NULL]
        if tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[3].isnumeric():
            if tokens[2] in ["Gen", "GenericKD"] or len(tokens[2]) <= 2:
                fmt = [PRE, FAM, SUF, SUF]
            elif tokens[2].isupper() and len(tokens[2]) <= 3:
                fmt = [PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        elif len(tokens[2]) <= 3 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF]
        elif tokens[3] == "Gen" or tokens[3].isnumeric() or tokens[3].isupper():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, PRE, PRE, UNK, UNK, SUF]
        if tokens[4] == "Gen" or tokens[4].isnumeric() or (len(tokens[4]) <= 2 and tokens[4] != "VB"):
            if tokens[3].isnumeric() or len(tokens[3]) <= 2:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK@TOK
    def parse_fmt6(self, tokens):
        if tokens[2] == "Heur":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt7(self, tokens):
        if re.match(r"[0-9A-F]{8}", tokens[4]):
            if tokens[3].isnumeric():
                fmt = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[3].isupper() and len(tokens[3]) <= 3:
                fmt = [PRE, PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF]
        elif tokens[2] == "CVE":
            fmt = [PRE, PRE, VULN, VULN, VULN]
        elif re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, SUF]
        elif "plugin" in [tokens[2].lower(), tokens[3].lower(), tokens[4].lower()]:
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            if tokens[2].isnumeric() or tokens[2] in ["Dropper", "Based"]:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            elif len(tokens[2]) <= 2 and tokens[2] != "VB":
                fmt = [PRE, FAM, SUF, SUF, SUF]
            elif tokens[2] == "Gen":
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].islower():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[3]) == 2:
            if re.match(r"V[0-9]", tokens[3]):
                fmt = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[1].lower() == "aol":
                fmt = [PRE, PRE, PRE, SUF, SUF]
            elif tokens[3].lower() == "vb":
                fmt = [PRE, PRE, PRE, PRE, SUF]
            elif tokens[2] == "VB":
                fmt = [PRE, PRE, FAM, SUF, SUF]
            elif len(tokens[2]) <= 3:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[4].isnumeric():
            if len(tokens[3]) <= 3:
                if len(tokens[2]) <= 3:
                    fmt = [PRE, FAM, SUF, SUF, SUF]
                else:
                    fmt = [PRE, PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_fmt8(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif tokens[3].isupper():
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
        elif tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt
