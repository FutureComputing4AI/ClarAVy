from claravy.taxonomy import *


class Parse_Avast: # Same company as AvastMobile. AVG is a subsidiary of Avast.

    def __init__(self):
        self.parse_fmt = {
            "TOK:TOK-TOK [TOK]": self.parse_fmt1,
            "TOK:TOK-TOK": self.parse_fmt2,
            "TOK:TOK": self.parse_fmt3,
            "TOK:TOK [TOK]": self.parse_fmt4,
            "TOK [TOK]": self.parse_fmt5,
            "TOK": self.parse_fmt6,
            "TOK:TOK-TOK {TOK}": self.parse_fmt7,
            "TOK-TOK": self.parse_fmt8,
            "TOK:TOK-TOK@TOK [TOK]": self.parse_fmt9,
            "TOK/TOK-TOK": self.parse_fmt10,
            "TOK:TOK-TOK-TOK-TOK [TOK]": self.parse_fmt11,
        }


    # TOK:TOK-TOK [TOK]
    def parse_fmt1(self, tokens):
        return [PRE, FAM, SUF, CAT, NULL]

    #TOK:TOK-TOK
    def parse_fmt2(self, tokens):
        return [PRE, FAM, SUF]

    # TOK:TOK
    def parse_fmt3(self, tokens):
        return [PRE, FAM]

    # TOK:TOK [TOK]
    def parse_fmt4(self, tokens):
        return [PRE, FAM, CAT, NULL]

    # TOK [TOK]
    def parse_fmt5(self, tokens):
        fmt = [UNK, CAT, NULL]
        if tokens[0].startswith("FileRep"):
            fmt = [PRE, CAT, NULL]
        else:
            fmt = [FAM, CAT, NULL]
        return fmt

    # TOK
    def parse_fmt6(self, tokens):
        fmt = [UNK]
        if tokens[0].startswith("FileRep"):
            fmt = [PRE]
        else:
            fmt = [FAM]
        return fmt

    #TOK:TOK-TOK {TOK}
    def parse_fmt7(self, tokens):
        return [CAT, PRE, PRE, UNK, NULL]

    # TOK-TOK
    def parse_fmt8(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1] == "gen" or tokens[1].isnumeric() or len(tokens[1]) == 1:
            fmt = [FAM, SUF]
        elif tokens[0].isupper(): # Bad format
            fmt = [UNK, UNK]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK:TOK-TOK@TOK [TOK]
    def parse_fmt9(self, tokens):
        return [CAT, FAM, SUF, UNK, CAT, NULL]

    # TOK/TOK-TOK
    def parse_fmt10(self, tokens):
        return [FAM, FAM, SUF]

    # TOK:TOK-TOK-TOK-TOK [TOK]
    def parse_fmt11(self, tokens):
        return [PRE, VULN, VULN, VULN, SUF, CAT, SUF]
