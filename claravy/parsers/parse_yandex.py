from claravy.taxonomy import *


class Parse_Yandex: # Acquired Agnitum, May rely on Sophos' signatures in some detections

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK!TOK": self.parse_delim_fmt1,
            "TOK.TOK!": self.parse_delim_fmt2,
            "TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK.TOK!TOK+TOK": self.parse_delim_fmt6,
            "TOK.TOK!TOK/TOK": self.parse_delim_fmt7,
        }

    # TOK.TOK!TOK
    def parse_delim_fmt1(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK!
    def parse_delim_fmt2(self, tokens):
        return [CAT, FAM, NULL]

    # TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[0] == "Packer":
            tax = [PRE, PACK, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        if tokens[3].isnumeric() and tokens[2].startswith("b"):
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[2] == "Gen" or tokens[2].isnumeric() or len(tokens[2]) == 1:
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[1].isupper():
                tax = [PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF, SUF]
        elif tokens[2].isupper() and tokens[2] != "VB":
            tax = [PRE, UNK, UNK, SUF] # Bad format
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        tax = [CAT, UNK, UNK, SUF]
        if tokens[2] == "Gen":
            tax = [CAT, FAM, SUF, SUF]
        else:
            tax = [CAT, PRE, FAM, SUF]
        return tax

    # TOK.TOK!TOK+TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK/TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, FAM, SUF, SUF]
