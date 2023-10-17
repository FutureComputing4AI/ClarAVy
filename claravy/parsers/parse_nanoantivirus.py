import re
from claravy.taxonomy import *


class Parse_Nanoantivirus:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK-TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK-TOK-TOK.TOK": self.parse_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [CAT, TGT, FAM, SUF]

    # TOK.TOK.TOK-TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[3]):
            fmt = [CAT, TGT, PRE, VULN, SUF]
        elif re.match(r"^MS[0-9]+$", tokens[2]) and tokens[3].isnumeric():
            fmt = [CAT, TGT, VULN, VULN, SUF]
        elif tokens[2].lower() in ["gen", "heuristic"]:
            fmt = [CAT, TGT, SUF, UNK, SUF]
        elif tokens[3].lower() in ["gen", "heuristic"]:
            fmt = [CAT, TGT, FAM, SUF, SUF]
        elif tokens[3].islower() or tokens[3].isnumeric():
            fmt = [CAT, TGT, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, UNK, UNK, SUF] # TODO: Bad format but might be able to be parsed more
        return fmt

    # TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [CAT, UNK, SUF]
        if re.match(r"CVE[0-9]+", tokens[1]):
            fmt = [CAT, VULN, SUF]
        elif tokens[1].isupper() and tokens[1] != "VB" and not any([c.isdigit() for c in tokens[1]]):
            fmt = [CAT, SUF, SUF]
        else:
            fmt = [CAT, FAM, SUF]
        return fmt

    # TOK.TOK.TOK-TOK-TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, UNK, SUF]
        if tokens[2].lower() in ["cve", "can"] and tokens[3].isnumeric() and tokens[4].isnumeric():
            fmt = [CAT, TGT, VULN, VULN, VULN, SUF]
        elif tokens[2] == "Gen":
            fmt = [CAT, TGT, PRE, PRE, PRE, SUF]
        else:
            fmt = [CAT, TGT, UNK, UNK, UNK, SUF] # TODO: Bad format but might be able to be parsed more
        return fmt

