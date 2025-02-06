from claravy.taxonomy import *


class Parse_Avg: # Subsidiary of Avast

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK:TOK-TOK [TOK]": self.parse_delim_fmt1,
            "TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK/TOK.TOK": self.parse_delim_fmt5,
            "TOK:TOK-TOK": self.parse_delim_fmt6,
            "TOK_TOK.TOK": self.parse_delim_fmt7,
            "TOK": self.parse_delim_fmt8,
            "TOK [TOK]": self.parse_delim_fmt9,
            "TOK:TOK [TOK]": self.parse_delim_fmt10,
            "TOK:TOK": self.parse_delim_fmt11,
            "TOK.TOK_TOK.TOK": self.parse_delim_fmt12,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt13,
            "TOK: TOK TOK": self.parse_delim_fmt14,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt15,
            "TOK-TOK/TOK.TOK": self.parse_delim_fmt16,
            "TOK/TOK{TOK}": self.parse_delim_fmt17,
            "TOK TOK": self.parse_delim_fmt18,
            "TOK-TOK/TOK": self.parse_delim_fmt19,
            "TOK TOK TOK/TOK{TOK}": self.parse_delim_fmt20,
            "TOK/TOK_TOK.TOK": self.parse_delim_fmt21,
            "TOK-TOK.TOK": self.parse_delim_fmt22,
            "TOK-TOK": self.parse_delim_fmt23,
            "TOK/TOK{TOK?}": self.parse_delim_fmt24,
            "TOK/TOK{TOK+TOK}": self.parse_delim_fmt25,
            "TOK/TOK.TOK.TOK_TOK": self.parse_delim_fmt26,
            "TOK_TOK": self.parse_delim_fmt27,
            "TOK/TOK.TOK{TOK}": self.parse_delim_fmt28,
        }

    # TOK:TOK-TOK [TOK]
    def parse_delim_fmt1(self, tokens):
        return [FILE, FAM, SUF, CAT, NULL]

    # TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isupper() or tokens[1].isnumeric() or tokens[1].islower():
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK/TOK
    def parse_delim_fmt3(self, tokens):
        return [FILE, FAM]

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[1].isupper() and tokens[1] != "VB":
            tax = [PRE, SUF, SUF]
        elif tokens[1].startswith("Generic"):
            tax = [PRE, PRE, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        else:
            tax = [UNK, FAM, SUF] # Unlear Skodna and Luhe tokens
        return tax

    # TOK/TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [FILE, FAM, SUF]

    # TOK:TOK-TOK
    def parse_delim_fmt6(self, tokens):
        return [PRE, FAM, SUF]

    # TOK_TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [FAM, SUF, SUF]

    # TOK
    def parse_delim_fmt8(self, tokens):
        return [FAM]

    # TOK [TOK]
    def parse_delim_fmt9(self, tokens):
        tax = [UNK, UNK, NULL]
        if tokens[0].startswith("FileRep"):
            tax = [PRE, PRE, NULL]
        else:
            tax = [FAM, SUF, SUF]
        return tax

    # TOK:TOK [TOK]
    def parse_delim_fmt10(self, tokens):
        return [FILE, FAM, CAT, NULL]

    # TOK:TOK
    def parse_delim_fmt11(self, tokens):
        return [FILE, FAM]

    # TOK.TOK_TOK.TOK
    def parse_delim_fmt12(self, tokens):
        return [UNK, FAM, SUF, SUF] # Unclear Skodna token

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt13(self, tokens):
        tax = [UNK, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].isupper():
            tax = [UNK, FAM, SUF, SUF]
        else: # Bad format w/ Skodna, Luhe tokens
            tax = [UNK, UNK, UNK, SUF]
        return tax

    # TOK: TOK TOK
    def parse_delim_fmt14(self, tokens):
        return [PRE, PRE, PRE]

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt15(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or len(tokens[2]) <= 2 or tokens[2].isupper():
            tax = [PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK-TOK/TOK.TOK
    def parse_delim_fmt16(self, tokens):
        return [PRE, CAT, FAM, SUF]

    # TOK/TOK{TOK}
    def parse_delim_fmt17(self, tokens):
        return [PRE, UNK, SUF, NULL]

    # TOK TOK
    def parse_delim_fmt18(self, tokens):
        tax = [UNK, UNK]
        if tokens[0] == "unknown":
            tax = [UNK, UNK]
        elif tokens[1].isnumeric() or tokens[1].isupper() or tokens[1].islower():
            tax = [FAM, SUF]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK-TOK/TOK
    def parse_delim_fmt19(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[2].isnumeric():
            tax = [FAM, SUF, SUF]
        else:
            tax = [PRE, CAT, FAM]
        return tax

    # TOK TOK TOK/TOK{TOK}
    def parse_delim_fmt20(self, tokens):
        return [PRE, PRE, FILE, UNK, SUF, NULL]

    # TOK/TOK_TOK.TOK
    def parse_delim_fmt21(self, tokens):
        return [CAT, PRE, SUF, SUF]

    # TOK-TOK.TOK
    def parse_delim_fmt22(self, tokens):
        tax = [UNK, UNK, SUF]
        if tokens[2].isnumeric():
            tax = [FAM, FAM, SUF]
        elif tokens[0] == "Rootkit":
            tax = [CAT, FAM, SUF]
        else: # Bad format
            tax = [UNK, UNK, SUF]
        return tax

    # TOK-TOK
    def parse_delim_fmt23(self, tokens):
        tax = [UNK, UNK]
        if tokens[0].isupper(): # Bad format
            tax = [UNK, UNK]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF]
        elif tokens[0] == "Rootkit":
            tax = [CAT, FAM]
        elif tokens[1] == "Obfuscated":
            tax = [PRE, PRE]
        elif tokens[1] == "gen":
            tax = [FAM, SUF]
        elif len(tokens[1]) == 1:
            tax = [UNK, UNK]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK/TOK{TOK?}
    def parse_delim_fmt24(self, tokens):
        return [FILE, UNK, SUF, NULL]

    # TOK/TOK{TOK+TOK}
    def parse_delim_fmt25(self, tokens):
        return [FILE, UNK, SUF, SUF, NULL]

    # TOK/TOK.TOK.TOK_TOK
    def parse_delim_fmt26(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK_TOK
    def parse_delim_fmt27(self, tokens):
        return [FAM, FAM]

    # TOK/TOK.TOK{TOK}
    def parse_delim_fmt28(self, tokens):
        return [FILE, UNK, SUF, SUF, NULL]
