from claravy.taxonomy import *


class Parse_Comodo:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt2,
            "TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK@#TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt6,
            "TOK.TOK.TOK.~TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK.TOK.~TOK": self.parse_delim_fmt8,
            "TOK.TOK.TOK": self.parse_delim_fmt9,
            "TOK.TOK.TOK.TOK.~TOK@TOK": self.parse_delim_fmt10,
            "TOK.TOK.TOK.~TOK@TOK": self.parse_delim_fmt11,
            "TOK.TOK": self.parse_delim_fmt12,
            "TOK.TOK!": self.parse_delim_fmt13,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [UNK, FILE, UNK, SUF]
        if tokens[0] == "Packed":
            tax = [PRE, FILE, PACK, SUF]
        else:
            tax = [PRE, FILE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, FILE, UNK, SUF, SUF]

        if tokens[0] == "Packed":
            tax = [PRE, FILE, PACK, SUF, SUF]
        else:
            tax = [PRE, FILE, FAM, SUF, SUF]
        return tax

    # TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, FILE, CAT, FAM, SUF]

    # TOK@#TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, SUF]

    # TOK.TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, FILE, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.~TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK.TOK.TOK.TOK.~TOK
    def parse_delim_fmt8(self, tokens):
        return [PRE, FILE, CAT, FAM, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt9(self, tokens):
        if tokens[1] == "Pck":
            tax = [PRE, PRE, PACK]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif tokens[2].isnumeric() or tokens[2] == "Gen":
            tax = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK.~TOK@TOK
    def parse_delim_fmt10(self, tokens):
        return [PRE, FILE, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.~TOK@TOK
    def parse_delim_fmt11(self, tokens):
        return [CAT, FILE, FAM, SUF, SUF]

    # TOK.TOK
    def parse_delim_fmt12(self, tokens):
        if tokens[0] == "Heur":
            tax = [PRE, PRE]
        elif len(tokens[1]) <= 2 or tokens[1].isnumeric() or tokens[1].isupper() or tokens[1].islower():
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK.TOK!
    def parse_delim_fmt13(self, tokens):
        return self.parse_delim_fmt12(tokens) + [NULL]

