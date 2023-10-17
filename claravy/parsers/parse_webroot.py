from claravy.taxonomy import *


class Parse_Webroot:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[2].lower() == "gen" or tokens[2].islower():
            fmt = [PRE, FAM, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF]
        elif tokens[2].isnumeric() or tokens[2].isupper():
            fmt = [PRE, UNK, SUF] # Bad format
        else:
            fmt = [PRE, UNK, UNK] # Very bad format - can't tell PRE from FAM
        return fmt

    # TOK.TOK
    def parse_fmt2(self, tokens):
        return [PRE, FAM]

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        if tokens[3] == "Gen" or tokens[3].islower() or tokens[3].isnumeric():
            fmt = [PRE, PRE, FAM, SUF]
        elif len(tokens[3]) <= 2 and tokens[3] != "VB":
            fmt = [PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, UNK, UNK] # Bad format
        return fmt
