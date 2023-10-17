from claravy.taxonomy import *


class Parse_Sophos: # Acuired Invincea

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK-TOK": self.parse_fmt1,
            "TOK (TOK)": self.parse_fmt2,
            "TOK": self.parse_fmt3,
            "TOK TOK TOK (TOK)": self.parse_fmt4,
            "TOK TOK (TOK)": self.parse_fmt5,
            "TOK TOK": self.parse_fmt6,
            "TOK/TOK-TOK + TOK/TOK-TOK": self.parse_fmt7,
            "TOK TOK TOK TOK (TOK)": self.parse_fmt8,
            "TOK TOK TOK": self.parse_fmt9,
            "TOK TOK-TOK TOK": self.parse_fmt10,
            "TOK/TOK": self.parse_fmt11,
            "TOK TOK-TOK TOK (TOK)": self.parse_fmt12,
        }

    # TOK/TOK-TOK
    def parse_fmt1(self, tokens):
        return [PRE, FAM, SUF]

    # TOK (TOK)
    def parse_fmt2(self, tokens):
        return [FAM, CAT, NULL]

    # TOK
    def parse_fmt3(self, tokens):
        return [FAM]

    # TOK TOK TOK (TOK)
    def parse_fmt4(self, tokens):
        return [UNK, UNK, UNK, CAT, NULL] # Really bad format - not sure if can be improved

    # TOK TOK (TOK)
    def parse_fmt5(self, tokens):
        return [UNK, UNK, CAT, NULL] # Really bad format - not sure if can be improved

    # TOK TOK
    def parse_fmt6(self, tokens):
        return [UNK, UNK] # Really bad format - not sure if can be improved

    # TOK/TOK-TOK + TOK/TOK-TOK
    def parse_fmt7(self, tokens):
        return [PRE, PRE, SUF, PRE, FAM, SUF]

    # TOK TOK TOK TOK (TOK)
    def parse_fmt8(self, tokens):
        return [UNK, UNK, UNK, UNK, CAT, NULL] # Really bad format - not sure if can be improved

    # TOK TOK TOK
    def parse_fmt9(self, tokens):
        return [UNK, UNK, UNK] # Really bad format - not sure if can be improved

    # TOK TOK-TOK TOK
    def parse_fmt10(self, tokens):
        return [UNK, UNK, UNK, UNK] # Really bad format - not sure if can be improved

    # TOK/TOK
    def parse_fmt11(self, tokens):
        fmt = [PRE, UNK]
        if tokens[1].isnumeric():
            fmt = [PRE, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK TOK-TOK TOK (TOK)
    def parse_fmt12(self, tokens):
        return [UNK, UNK, UNK, UNK, SUF, NULL] # Really bad format - not sure if can be improved
