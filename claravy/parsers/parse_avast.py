from claravy.taxonomy import *


class Parse_Avast: # Same company as AvastMobile. AVG is a subsidiary of Avast.

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK-TOK [TOK]": self.parse_delim_fmt1,
            "TOK:TOK-TOK": self.parse_delim_fmt2,
            "TOK:TOK": self.parse_delim_fmt3,
            "TOK:TOK [TOK]": self.parse_delim_fmt4,
            "TOK [TOK]": self.parse_delim_fmt5,
            "TOK": self.parse_delim_fmt6,
            "TOK:TOK-TOK {TOK}": self.parse_delim_fmt7,
            "TOK-TOK": self.parse_delim_fmt8,
            "TOK:TOK-TOK@TOK [TOK]": self.parse_delim_fmt9,
            "TOK/TOK-TOK": self.parse_delim_fmt10,
            "TOK:TOK-TOK-TOK-TOK [TOK]": self.parse_delim_fmt11,
        }


    # TOK:TOK-TOK [TOK]
    def parse_delim_fmt1(self, tokens):
        return [PRE, FAM, SUF, CAT, NULL]

    #TOK:TOK-TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM, SUF]

    # TOK:TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, FAM]

    # TOK:TOK [TOK]
    def parse_delim_fmt4(self, tokens):
        return [PRE, FAM, CAT, NULL]

    # TOK [TOK]
    def parse_delim_fmt5(self, tokens):
        tax = [UNK, CAT, NULL]
        if tokens[0].startswith("FileRep"):
            tax = [PRE, CAT, NULL]
        else:
            tax = [FAM, CAT, NULL]
        return tax

    # TOK
    def parse_delim_fmt6(self, tokens):
        tax = [UNK]
        if tokens[0].startswith("FileRep"):
            tax = [PRE]
        else:
            tax = [FAM]
        return tax

    #TOK:TOK-TOK {TOK}
    def parse_delim_fmt7(self, tokens):
        return [CAT, PRE, PRE, UNK, NULL]

    # TOK-TOK
    def parse_delim_fmt8(self, tokens):
        tax = [UNK, UNK]
        if tokens[1] == "gen" or tokens[1].isnumeric() or len(tokens[1]) == 1:
            tax = [FAM, SUF]
        elif tokens[0].isupper(): # Bad format
            tax = [UNK, UNK]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK:TOK-TOK@TOK [TOK]
    def parse_delim_fmt9(self, tokens):
        return [CAT, FAM, SUF, UNK, CAT, NULL]

    # TOK/TOK-TOK
    def parse_delim_fmt10(self, tokens):
        return [FAM, FAM, SUF]

    # TOK:TOK-TOK-TOK-TOK [TOK]
    def parse_delim_fmt11(self, tokens):
        return [PRE, VULN, VULN, VULN, SUF, CAT, SUF]
