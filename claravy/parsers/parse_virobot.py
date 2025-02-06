from claravy.taxonomy import *


class Parse_Virobot: # Seems to use Bitdefender's engine and own engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK_TOK_TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK[TOK]": self.parse_delim_fmt6,
            "TOK.TOK.TOK[TOK]": self.parse_delim_fmt7,
            "TOK.TOK.TOK.TOK[TOK]": self.parse_delim_fmt8,
            "TOK.TOK.TOK.TOK.TOK.TOK[TOK]": self.parse_delim_fmt9,
            "TOK.TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt10,
            "TOK.TOK.TOK.TOK-TOK.TOK.TOK": self.parse_delim_fmt11,
        }

    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if tokens[0] == "Packed":
            tax = [PRE, PRE, PACK]
        elif tokens[2].isnumeric() or len(tokens[2]) <= 2 or tokens[2] == "Gen":
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        if len(tokens[2]) <= 2 and tokens[2] != "VB":
            if tokens[3].isnumeric() or tokens[3] == "Gen":
                tax = [CAT, FAM, SUF, SUF, SUF]
            else:
                tax = [CAT, FILE, SUF, FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1] != "VB":
            tax = [PRE, SUF, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[1] == "Win32":
            tax = [PRE, FILE, FAM, SUF, SUF]
        else:
            tax = [PRE, UNK, UNK, SUF, SUF] # Bad format
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[1]) <= 2:
            tax = [PRE, SUF, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [CAT, FILE, UNK, UNK, SUF, SUF]
        if len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [CAT, FILE, SUF, FAM, SUF, SUF]
        else:
            tax = [CAT, FILE, UNK, UNK, SUF, SUF] # Bad format
        return tax

    # TOK.TOK_TOK_TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, UNK, SUF] # All Geno iframe

    # TOK.TOK.TOK.TOK.TOK[TOK]
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF, UNK, NULL]
        if tokens[3].isnumeric() or tokens[3] == "Gen" or len(tokens[3]) == 1:
            if tokens[2].isnumeric() or tokens[2] == "Gen" or len(tokens[2]) == 1:
                tax = [PRE, FAM, SUF, SUF, SUF, SUF, NULL]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, NULL]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, NULL]
        if not tokens[5].islower():
            tax[5] = PACK
        return tax

    # TOK.TOK.TOK[TOK]
    def parse_delim_fmt7(self, tokens):
        tax = [UNK, UNK, UNK, UNK, NULL]
        if any(filter(str.islower, tokens[2])):
            if tokens[2] in ["Gen", "Dam", "based", "Generic"]:
                if tokens[2] in ["based", "Generic"] or tokens[1].isnumeric():
                    tax = [UNK, SUF, SUF, SUF, NULL]
                else:
                    tax = [PRE, FAM, SUF, SUF, NULL]
            else:
                tax = [PRE, PRE, FAM, SUF, NULL]
        else:
            tax = [PRE, FAM, SUF, SUF, NULL]
        return tax

    # TOK.TOK.TOK.TOK[TOK]
    def parse_delim_fmt8(self, tokens):
        tax = self.parse_delim_fmt3(tokens) + [SUF, NULL]
        if not tokens[4].islower():
            tax[4] = PACK
        return tax

    # TOK.TOK.TOK.TOK.TOK.TOK[TOK]
    def parse_delim_fmt9(self, tokens):
        tax = self.parse_delim_fmt4(tokens) + [SUF, NULL]
        if not tokens[6].islower():
            tax[6] = PACK
        return tax

    # TOK.TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt10(self, tokens):
        return [CAT, FILE, SUF, PRE, FAM, SUF]

    # TOK.TOK.TOK.TOK-TOK.TOK.TOK
    def parse_delim_fmt11(self, tokens):
        return [CAT, FILE, SUF, PRE, FAM, SUF, SUF]
