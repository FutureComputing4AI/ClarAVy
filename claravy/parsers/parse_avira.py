import re
from claravy.taxonomy import *


class Parse_Avira: # Renamed from Antivir. Format somewhat similar to TheHacker, but probably not related. Partnership with F-Secure.

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_fmt2,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK/TOK": self.parse_fmt4,
            "TOK.TOK": self.parse_fmt5,
        }

    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric() or re.match(r"^Gen[0-9]*$", tokens[2]):
            fmt = [PRE, FAM, SUF]
        else: # Bad format
            fmt = [PRE, UNK, UNK]
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [CAT, UNK, UNK, SUF]
        if tokens[2].islower() or tokens[2].isnumeric() or len(tokens[2]) <= 2:
            fmt = [CAT, FAM, SUF, SUF]
        elif tokens[2].isupper() and len(tokens[2]) <= 4:
            fmt = [CAT, FAM, SUF, SUF]
        else:
            fmt = [CAT, CAT, FAM, SUF]
        return fmt

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if len(tokens[2]) == 1:
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif not tokens[3].isupper() and not tokens[3].islower() and not tokens[3].isnumeric():
            if tokens[4] == "Gen":
                fmt = [PRE, PRE, PRE, PRE, SUF]
            elif tokens[2].isnumeric() or tokens[2].islower() or len(tokens[2]) <= 2:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else: # Bad format
                fmt = [PRE, UNK, UNK, UNK, SUF]
        elif tokens[2].isnumeric() or tokens[2].islower():
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[2].isupper() and len(tokens[2]) == 3: # Bad format
            fmt = [PRE, UNK, UNK, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK/TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric():
            fmt = [PRE, SUF]
        elif tokens[1].islower() or tokens[1].isupper(): # Bad format
            fmt = [UNK, UNK]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0].islower() or tokens[1].islower(): # Bad format
            fmt = [UNK, UNK]
        elif tokens[1].isnumeric() or len(tokens[1]) == 1 or tokens[1].isupper():
            fmt = [FAM, SUF]
        else: # Bad format
            fmt = [UNK, UNK]
        return fmt
