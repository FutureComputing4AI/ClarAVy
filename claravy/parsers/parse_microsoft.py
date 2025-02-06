import re
from claravy.taxonomy import *


class Parse_Microsoft:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK:TOK/TOK": self.parse_delim_fmt2,
            "TOK:TOK/TOK.TOK!TOK": self.parse_delim_fmt3,
            "TOK:TOK/TOK!TOK": self.parse_delim_fmt4,
            "TOK:TOK/TOK.TOK@TOK": self.parse_delim_fmt5,
        }

    # TOK:TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [CAT, FILE, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF]
        return tax

    # TOK:TOK/TOK
    def parse_delim_fmt2(self, tokens):
        tax = [CAT, FILE, UNK]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN]
        else:
            tax = [CAT, FILE, FAM]
        return tax

    # TOK:TOK/TOK.TOK!TOK
    def parse_delim_fmt3(self, tokens):
        tax = [CAT, FILE, UNK, SUF, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF, SUF]
        return tax

    # TOK:TOK/TOK!TOK
    def parse_delim_fmt4(self, tokens):
        tax = [CAT, FILE, UNK, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF]
        return tax

    # TOK:TOK/TOK.TOK@TOK
    def parse_delim_fmt5(self, tokens):
        tax = [CAT, FILE, UNK, SUF, SUF]
        if re.match(r"^MS[0-9]+$", tokens[2]):
            tax = [CAT, FILE, VULN, SUF, SUF]
        else:
            tax = [CAT, FILE, FAM, SUF, SUF]
        return tax
