import re
from claravy.taxonomy import *


class Parse_Tencent:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK-TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK_TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK.TOK. TOK.TOK": self.parse_delim_fmt7,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt8,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK-TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK_TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, PRE, SUF, PRE, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if tokens[3] == "Gen" or len(tokens[3]) <= 2:
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [FILE, CAT, UNK, UNK, SUF]
        if re.match(r"^Ms[0-9]+", tokens[2]) and tokens[3].isnumeric():
            tax = [FILE, CAT, VULN, VULN, SUF]
        elif tokens[3] == "based":
            tax = [FILE, CAT, FAM, SUF, SUF]
        elif tokens[2].lower() == "ps" and tokens[3].lower() == "mpc":
            tax = [FILE, CAT, FAM, FAM, SUF]
        elif len(tokens[2]) <= 2:
            tax = [FILE, CAT, SUF, FAM, SUF]
        elif tokens[3].isnumeric():
            tax = [FILE, CAT, FAM, SUF, SUF]
        else:
            tax = [FILE, CAT, UNK, UNK, SUF] # Bad format
        return tax

    # TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        if len(tokens[0]) == 1:
            tax = [SUF, PRE, FAM]
        elif len(tokens[2]) == 1 or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK. TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]
    
