from claravy.taxonomy import *


class Parse_Thehacker: # Format somewhat similar to Antivir/Avira, but seems to be unrelated

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK-TOK-TOK-TOK": self.parse_delim_fmt3,
            "TOK_TOK": self.parse_delim_fmt4,
            "TOK/TOK-TOK-TOK": self.parse_delim_fmt5,
        }

    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if len(tokens[2]) == 1 or tokens[2].islower() or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK-TOK-TOK-TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, PRE, PRE, SUF]

    # TOK_TOK
    def parse_delim_fmt4(self, tokens):
        if tokens[0] == "Posible":
            tax = [PRE, PRE]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK/TOK-TOK-TOK
    def parse_delim_fmt5(self, tokens):
        if tokens[1] == "CVE" and tokens[2].isnumeric() and tokens[3].isnumeric():
            tax = [PRE, VULN, VULN, VULN]
        elif tokens[2] == "Heuristic":
            tax = [PRE, PRE, PRE, SUF]
        else:
            tax = [UNK, UNK, UNK, SUF] # Bad format
        return tax
