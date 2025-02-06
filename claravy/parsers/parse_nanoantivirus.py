import re
from claravy.taxonomy import *


class Parse_Nanoantivirus:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK-TOK-TOK.TOK": self.parse_delim_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [CAT, FILE, UNK, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[3]):
            tax = [CAT, FILE, PRE, VULN, SUF]
        elif re.match(r"^MS[0-9]+$", tokens[2]) and tokens[3].isnumeric():
            tax = [CAT, FILE, VULN, VULN, SUF]
        elif tokens[2].lower() in ["gen", "heuristic"]:
            tax = [CAT, FILE, SUF, UNK, SUF]
        elif tokens[3].lower() in ["gen", "heuristic"]:
            tax = [CAT, FILE, FAM, SUF, SUF]
        elif tokens[3].islower() or tokens[3].isnumeric():
            tax = [CAT, FILE, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, UNK, UNK, SUF] # TODO: Bad format but might be able to be parsed more
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [CAT, UNK, SUF]
        if re.match(r"CVE[0-9]+", tokens[1]):
            tax = [CAT, VULN, SUF]
        elif tokens[1].isupper() and tokens[1] != "VB" and not any([c.isdigit() for c in tokens[1]]):
            tax = [CAT, SUF, SUF]
        else:
            tax = [CAT, FAM, SUF]
        return tax

    # TOK.TOK.TOK-TOK-TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [CAT, FILE, UNK, UNK, UNK, SUF]
        if tokens[2].lower() in ["cve", "can"] and tokens[3].isnumeric() and tokens[4].isnumeric():
            tax = [CAT, FILE, VULN, VULN, VULN, SUF]
        elif tokens[2] == "Gen":
            tax = [CAT, FILE, PRE, PRE, PRE, SUF]
        else:
            tax = [CAT, FILE, UNK, UNK, UNK, SUF] # TODO: Bad format but might be able to be parsed more
        return tax

