from claravy.taxonomy import *


class Parse_Virobot: # Seems to use Bitdefender's engine and own engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK_TOK_TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK[TOK]": self.parse_fmt6,
            "TOK.TOK.TOK[TOK]": self.parse_fmt7,
            "TOK.TOK.TOK.TOK[TOK]": self.parse_fmt8,
            "TOK.TOK.TOK.TOK.TOK.TOK[TOK]": self.parse_fmt9,
            "TOK.TOK.TOK.TOK-TOK.TOK": self.parse_fmt10,
            "TOK.TOK.TOK.TOK-TOK.TOK.TOK": self.parse_fmt11,
        }

    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if tokens[0] == "Packed":
            fmt = [PRE, PRE, PACK]
        elif tokens[2].isnumeric() or len(tokens[2]) <= 2 or tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        if len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[3].isnumeric() or tokens[3] == "Gen":
                fmt = [CAT, FAM, SUF, SUF, SUF]
            else:
                fmt = [CAT, TGT, SUF, FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            fmt = [PRE, SUF, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[1] == "Win32":
            fmt = [PRE, TGT, FAM, SUF, SUF]
        else:
            fmt = [PRE, UNK, UNK, SUF, SUF] # Bad format
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[1]) <= 2:
            fmt = [PRE, SUF, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        fmt = [CAT, TGT, UNK, UNK, SUF, SUF]
        if len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [CAT, TGT, SUF, FAM, SUF, SUF]
        else:
            fmt = [CAT, TGT, UNK, UNK, SUF, SUF] # Bad format
        return fmt

    # TOK.TOK_TOK_TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, UNK, SUF] # All Geno iframe

    # TOK.TOK.TOK.TOK.TOK[TOK]
    def parse_fmt6(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, UNK, NULL]
        if tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                fmt = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        if not tokens[5].islower():
            fmt[5] = PACK
        return fmt

    # TOK.TOK.TOK[TOK]
    def parse_fmt7(self, tokens):
        fmt = [UNK, UNK, UNK, UNK, NULL]
        if any(filter(str.islower, tokens[2])):
            if tokens[2] in ["Gen", "Dam", "based", "Generic"]:
                if tokens[2] in ["based", "Generic"] or tokens[1].isnumeric():
                    fmt = [UNK, SUF, SUF, SUF, NULL]
                else:
                    fmt = [PRE, FAM, SUF, SUF, NULL]
            else:
                fmt = [PRE, PRE, FAM, SUF, NULL]
        else:
            fmt = [PRE, FAM, SUF, SUF, NULL]
        return fmt

    # TOK.TOK.TOK.TOK[TOK]
    def parse_fmt8(self, tokens):
        fmt = self.parse_fmt3(tokens) + [SUF, NULL]
        if not tokens[4].islower():
            fmt[4] = PACK
        return fmt

    # TOK.TOK.TOK.TOK.TOK.TOK[TOK]
    def parse_fmt9(self, tokens):
        fmt = self.parse_fmt4(tokens) + [SUF, NULL]
        if not tokens[6].islower():
            fmt[6] = PACK
        return fmt

    # TOK.TOK.TOK.TOK-TOK.TOK
    def parse_fmt10(self, tokens):
        return [CAT, TGT, SUF, PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK-TOK.TOK.TOK
    def parse_fmt11(self, tokens):
        return [CAT, TGT, SUF, PRE, FAM, SUF, SUF]
