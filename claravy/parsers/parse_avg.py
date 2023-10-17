from claravy.taxonomy import *


class Parse_Avg: # Subsidiary of Avast

    def __init__(self):
        self.parse_fmt = {
            "TOK:TOK-TOK [TOK]": self.parse_fmt1,
            "TOK.TOK": self.parse_fmt2,
            "TOK/TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
            "TOK/TOK.TOK": self.parse_fmt5,
            "TOK:TOK-TOK": self.parse_fmt6,
            "TOK_TOK.TOK": self.parse_fmt7,
            "TOK": self.parse_fmt8,
            "TOK [TOK]": self.parse_fmt9,
            "TOK:TOK [TOK]": self.parse_fmt10,
            "TOK:TOK": self.parse_fmt11,
            "TOK.TOK_TOK.TOK": self.parse_fmt12,
            "TOK.TOK.TOK.TOK": self.parse_fmt13,
            "TOK: TOK TOK": self.parse_fmt14,
            "TOK/TOK.TOK.TOK": self.parse_fmt15,
            "TOK-TOK/TOK.TOK": self.parse_fmt16,
            "TOK/TOK{TOK}": self.parse_fmt17,
            "TOK TOK": self.parse_fmt18,
            "TOK-TOK/TOK": self.parse_fmt19,
            "TOK TOK TOK/TOK{TOK}": self.parse_fmt20,
            "TOK/TOK_TOK.TOK": self.parse_fmt21,
            "TOK-TOK.TOK": self.parse_fmt22,
            "TOK-TOK": self.parse_fmt23,
            "TOK/TOK{TOK?}": self.parse_fmt24,
            "TOK/TOK{TOK+TOK}": self.parse_fmt25,
            "TOK/TOK.TOK.TOK_TOK": self.parse_fmt26,
            "TOK_TOK": self.parse_fmt27,
            "TOK/TOK.TOK{TOK}": self.parse_fmt28,
        }

    # TOK:TOK-TOK [TOK]
    def parse_fmt1(self, tokens):
        return [TGT, FAM, SUF, CAT, NULL]

    # TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isupper() or tokens[1].isnumeric() or tokens[1].islower():
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK/TOK
    def parse_fmt3(self, tokens):
        return [TGT, FAM]

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[1].isupper() and tokens[1] != "VB":
            fmt = [PRE, SUF, SUF]
        elif tokens[1].startswith("Generic"):
            fmt = [PRE, PRE, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [UNK, FAM, SUF] # Unlear Skodna and Luhe tokens
        return fmt

    # TOK/TOK.TOK
    def parse_fmt5(self, tokens):
        return [TGT, FAM, SUF]

    # TOK:TOK-TOK
    def parse_fmt6(self, tokens):
        return [PRE, FAM, SUF]

    # TOK_TOK.TOK
    def parse_fmt7(self, tokens):
        return [FAM, SUF, SUF]

    # TOK
    def parse_fmt8(self, tokens):
        return [FAM]

    # TOK [TOK]
    def parse_fmt9(self, tokens):
        fmt = [UNK, UNK, NULL]
        if tokens[0].startswith("FileRep"):
            fmt = [PRE, PRE, NULL]
        else:
            fmt = [FAM, SUF, SUF]
        return fmt

    # TOK:TOK [TOK]
    def parse_fmt10(self, tokens):
        return [TGT, FAM, CAT, NULL]

    # TOK:TOK
    def parse_fmt11(self, tokens):
        return [TGT, FAM]

    # TOK.TOK_TOK.TOK
    def parse_fmt12(self, tokens):
        return [UNK, FAM, SUF, SUF] # Unclear Skodna token

    # TOK.TOK.TOK.TOK
    def parse_fmt13(self, tokens):
        fmt = [UNK, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].isupper():
            fmt = [UNK, FAM, SUF, SUF]
        else: # Bad format w/ Skodna, Luhe tokens
            fmt = [UNK, UNK, UNK, SUF]
        return fmt

    # TOK: TOK TOK
    def parse_fmt14(self, tokens):
        return [PRE, PRE, PRE]

    # TOK/TOK.TOK.TOK
    def parse_fmt15(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or len(tokens[2]) <= 2 or tokens[2].isupper():
            fmt = [PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK-TOK/TOK.TOK
    def parse_fmt16(self, tokens):
        return [PRE, CAT, FAM, SUF]

    # TOK/TOK{TOK}
    def parse_fmt17(self, tokens):
        return [PRE, UNK, SUF, NULL]

    # TOK TOK
    def parse_fmt18(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0] == "unknown":
            fmt = [UNK, UNK]
        elif tokens[1].isnumeric() or tokens[1].isupper() or tokens[1].islower():
            fmt = [FAM, SUF]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK-TOK/TOK
    def parse_fmt19(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[2].isnumeric():
            fmt = [FAM, SUF, SUF]
        else:
            fmt = [PRE, CAT, FAM]
        return fmt

    # TOK TOK TOK/TOK{TOK}
    def parse_fmt20(self, tokens):
        return [PRE, PRE, TGT, UNK, SUF, NULL]

    # TOK/TOK_TOK.TOK
    def parse_fmt21(self, tokens):
        return [CAT, PRE, SUF, SUF]

    # TOK-TOK.TOK
    def parse_fmt22(self, tokens):
        fmt = [UNK, UNK, SUF]
        if tokens[2].isnumeric():
            fmt = [FAM, FAM, SUF]
        elif tokens[0] == "Rootkit":
            fmt = [CAT, FAM, SUF]
        else: # Bad format
            fmt = [UNK, UNK, SUF]
        return fmt

    # TOK-TOK
    def parse_fmt23(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0].isupper(): # Bad format
            fmt = [UNK, UNK]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF]
        elif tokens[0] == "Rootkit":
            fmt = [CAT, FAM]
        elif tokens[1] == "Obfuscated":
            fmt = [PRE, PRE]
        elif tokens[1] == "gen":
            fmt = [FAM, SUF]
        elif len(tokens[1]) == 1:
            fmt = [UNK, UNK]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK/TOK{TOK?}
    def parse_fmt24(self, tokens):
        return [TGT, UNK, SUF, NULL]

    # TOK/TOK{TOK+TOK}
    def parse_fmt25(self, tokens):
        return [TGT, UNK, SUF, SUF, NULL]

    # TOK/TOK.TOK.TOK_TOK
    def parse_fmt26(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK_TOK
    def parse_fmt27(self, tokens):
        return [FAM, FAM]

    # TOK/TOK.TOK{TOK}
    def parse_fmt28(self, tokens):
        return [TGT, UNK, SUF, SUF, NULL]
