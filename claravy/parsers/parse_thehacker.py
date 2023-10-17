from claravy.taxonomy import *


class Parse_Thehacker: # Format somewhat similar to Antivir/Avira, but seems to be unrelated

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_fmt2,
            "TOK/TOK-TOK-TOK-TOK": self.parse_fmt3,
            "TOK_TOK": self.parse_fmt4,
            "TOK/TOK-TOK-TOK": self.parse_fmt5,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK/TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if len(tokens[2]) == 1 or tokens[2].islower() or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK-TOK-TOK-TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, PRE, PRE, SUF]

    # TOK_TOK
    def parse_fmt4(self, tokens):
        if tokens[0] == "Posible":
            fmt = [PRE, PRE]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK/TOK-TOK-TOK
    def parse_fmt5(self, tokens):
        if tokens[1] == "CVE" and tokens[2].isnumeric() and tokens[3].isnumeric():
            fmt = [PRE, VULN, VULN, VULN]
        elif tokens[2] == "Heuristic":
            fmt = [PRE, PRE, PRE, SUF]
        else:
            fmt = [UNK, UNK, UNK, SUF] # Bad format
        return fmt
