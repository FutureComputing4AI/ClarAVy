import re
from claravy.taxonomy import *


class Parse_Antivir: # Renamed to Avira. Format similar to Thehacker but does not seem related.

    def __init__(self):
        self.parse_fmt = {
            "TOK/TOK.TOK": self.parse_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_fmt2,
            "TOK/TOK.TOK.TOK.TOK": self.parse_fmt3,
            "TOK/TOK": self.parse_fmt4,
            "TOK/TOK-TOK-TOK.TOK": self.parse_fmt5,
            "TOK/TOK.TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK #TOK": self.parse_fmt7,
            "TOK-TOK": self.parse_fmt8,
            "TOK": self.parse_fmt9,
            "TOK/TOK-TOK.TOK": self.parse_fmt10,
            "TOK_#TOK": self.parse_fmt11,
            "TOK/TOK.#TOK": self.parse_fmt12,
            "TOK.TOK": self.parse_fmt13,
            "TOK-TOK-TOK #TOK": self.parse_fmt14,
            "TOK-TOK (TOK)": self.parse_fmt15,
            "TOK/TOK-TOK.TOK.TOK": self.parse_fmt16,
            "TOK/TOK-TOK": self.parse_fmt17,
            "TOK/TOK.TOK-TOK": self.parse_fmt18,
            "TOK (TOK) #TOK": self.parse_fmt19,
            "TOK/TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt20,
            "_TOK_TOK_TOK": self.parse_fmt21,
            "TOK (TOK)": self.parse_fmt22,
        }


    # TOK/TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK]
        if len(tokens[2]) <= 4 or tokens[2][0].isnumeric() or tokens[2].islower():
            fmt = [PRE, FAM, SUF]
        # A few remaining labels have unclear formats
        return fmt

    # TOK/TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].islower():
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 and tokens[2].isupper():
            fmt = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2:
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Crypt":
            fmt = [PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if len(tokens[3]) <= 4 or tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isnumeric() or tokens[2].islower():
                fmt = [PRE, FAM, SUF, SUF, SUF]
            elif len(tokens[2]) <= 2 and tokens[2] != "VB":
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[3].isupper() or re.search(r"\d", tokens[3]):
            fmt = [PRE, PRE, FAM, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK/TOK
    def parse_fmt4(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0] == "PCK":
            fmt = [PRE, PACK]
        elif tokens[1].isnumeric(): # First token is very rarely FAM, mostly PRE
            fmt = [UNK, SUF]
        elif tokens[1].isupper() and (len(tokens[1]) <= 2 or not tokens[0].isupper()): # Another odd format
            fmt = [UNK, UNK]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK/TOK-TOK-TOK.TOK
    def parse_fmt5(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1].lower() in ["c", "cv", "cve", "can"] and tokens[2].isnumeric() and tokens[3].isnumeric():
            fmt = [PRE, VULN, VULN, VULN, SUF]
        elif tokens[3].startswith("base"):
            fmt = [PRE, FAM, FAM, SUF, SUF]
        # A few unusually formatted labels left over
        return fmt

    # TOK/TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, UNK, SUF]
        if tokens[1].lower() in ["c", "cv", "cve", "can"] and tokens[2].isnumeric() and tokens[3].isnumeric():
            fmt = [PRE, VULN, VULN, VULN, SUF, SUF]
        elif tokens[2].lower() in ["c", "cv", "cve", "can"] and tokens[3].isnumeric() and tokens[4].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isnumeric() or tokens[2].islower():
                fmt = [PRE, FAM, SUF, SUF, SUF, SUF]
            elif tokens[2].isupper() or (len(tokens[2]) <= 2 and tokens[2] != "VB"): # Unusual format
                fmt = [PRE, UNK, SUF, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isupper() or tokens[3] == "Gen":
            if len(tokens[2]) <= 2 and tokens[2] != "VB":
                fmt = [PRE, CAT, PRE, SUF, SUF, SUF]
            else:
                fmt = [PRE, CAT, FAM, SUF, SUF, SUF]
        elif len(tokens[2]) <= 1:
            fmt = [PRE, FAM, SUF, SUF, SUF, SUF]
        else:
            fmt = [CAT, CAT, PRE, FAM, SUF, SUF]
        return fmt

    # TOK #TOK
    def parse_fmt7(self, tokens):
        return [FAM, SUF]

    # TOK-TOK
    def parse_fmt8(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0] == "Trivial":
            if tokens[1].isnumeric():
                fmt = [PRE, SUF]
            else:
                fmt = [PRE, FAM]
        elif tokens[1].isnumeric() or tokens[1] == "based":
            if len(tokens[0]) <= 2:
                fmt = [UNK, SUF]
            else:
                fmt = [FAM, SUF]
        elif tokens[1] in ["Related", "Generic", "Trojan", "Small"]:
            fmt = [FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1].isupper():
            fmt = [FAM, SUF]
        elif tokens[0].isupper(): # Unusual label format
            fmt = [UNK, UNK]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK 
    def parse_fmt9(self, tokens):
        fmt = [UNK]
        if tokens[0].isupper(): # Some FAM, some SUF
            fmt = [UNK]
        elif tokens[0].isnumeric():
            fmt = [SUF]
        else:
            fmt = [FAM]
        return fmt

    # TOK/TOK-TOK.TOK
    def parse_fmt10(self, tokens):
        fmt = [PRE, UNK, UNK, UNK]
        if tokens[2].islower() or tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "EXP" and tokens[1].isnumeric() and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN, SUF]
        elif re.match(r"MS[0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN, SUF]
        elif tokens[1] == "BackDoor":
            fmt = [PRE, CAT, SUF, SUF]
        elif tokens[0] in ["SPR", "DOS", "APPL"]:
            fmt = [PRE, FAM, FAM, SUF]
        else: # TODO: Unsure how to parse remaining tokens
            fmt = [PRE, UNK, UNK, UNK]
        return fmt

    # TOK_#TOK
    def parse_fmt11(self, tokens):
        return [FAM, SUF]

    # TOK_#TOK
    def parse_fmt12(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK
    def parse_fmt13(self, tokens):
        fmt = [UNK, UNK]
        if len(tokens[1]) >= 3 and not tokens[1].isupper() and not tokens[1].isnumeric():
            if not tokens[0].isupper():
                if tokens[0] in ["Trivial", "Joke", "Stoned"]:
                    fmt = [PRE, FAM]
                elif "Macro" in tokens[0]:
                    fmt = [PRE, FAM]
                else:
                    fmt = [FAM, FAM]
            else:
                fmt = [PRE, FAM]
        elif tokens[1].isupper():
            fmt = [UNK, SUF]
        else:
            fmt = [FAM, SUF]
        return fmt

    # TOK-TOK-TOK #TOK
    def parse_fmt14(self, tokens):
        return [FAM, FAM, SUF, SUF]

    # TOK-TOK (TOK)
    def parse_fmt15(self, tokens):
        fmt = [UNK, UNK, SUF, NULL]
        if tokens[1].isnumeric():
            if tokens[0].isupper():
                fmt = [UNK, SUF, SUF, NULL]
            else:
                fmt = [FAM, SUF, SUF, NULL]
        elif tokens[0].isupper():
            fmt = [UNK, UNK, SUF, NULL]
        else:
            fmt = [FAM, FAM, SUF, SUF]
        return fmt

    # TOK/TOK-TOK.TOK.TOK
    def parse_fmt16(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[0] == "EXP" and tokens[1].isnumeric() and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN, SUF, SUF]
        elif re.match(r"MS[0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN, SUF, SUF]
        elif tokens[1] == "CVE": # Bad CVE format
            fmt = [PRE, UNK, UNK, SUF, SUF]
        elif tokens[2].islower(): # Unclear format
            fmt = [PRE, UNK, SUF, SUF, SUF]
        elif tokens[0] in ["SPR", "DOS", "APPL"]:
            if tokens[2].isnumeric(): # Unclear format
                fmt = [PRE, UNK, UNK, SUF, SUF]
            else:
                fmt = [PRE, FAM, FAM, SUF, SUF]
        elif not tokens[2].isupper() and not tokens[2].isnumeric():
            fmt = [PRE, FAM, FAM, SUF, SUF]
        else:
            fmt = [PRE, FAM, SUF, SUF, SUF]
        return fmt

    # TOK/TOK-TOK
    def parse_fmt17(self, tokens):
        if re.match(r"MS[0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN]
        elif len(tokens[2]) >= 3 and not tokens[2].isnumeric():
            if tokens[2].lower() == "based":
                fmt = [PRE, FAM, SUF]
            elif tokens[0].isnumeric() and tokens[1].isnumeric(): # Very unusual format
                fmt = [UNK, UNK, FAM]
            elif tokens[1] == "Trivial":
                fmt = [PRE, PRE, SUF]
            else:
                fmt = [PRE, FAM, FAM]
        else:
            fmt = [PRE, FAM, SUF]
        return fmt

    # TOK/TOK.TOK-TOK
    def parse_fmt18(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if re.match(r"[Cc][Vv][Ee][0-9]{4}", tokens[2]):
            fmt = [PRE, PRE, VULN, VULN]
        elif re.match(r"MS[0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN]
        # Remainer of labels do not contain families, unclear format
        return fmt

    # TOK (TOK) #TOK
    def parse_fmt19(self, tokens):
        return [FAM, SUF, SUF]

    # TOK/TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt20(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, UNK, UNK, SUF]
        if tokens[3].lower() == "cve" and tokens[4].isnumeric() and tokens[5].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"MS[0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, SUF, SUF]
        else: # Bad format, usually no FAM
            fmt = [PRE, UNK, UNK, UNK, UNK, SUF, SUF]
        return fmt

    # _TOK_TOK_TOK
    def parse_fmt21(self, tokens):
        return [NULL, SUF, SUF, SUF]

    # TOK (TOK)
    def parse_fmt22(self, tokens):
        fmt = [UNK, UNK, NULL]
        if tokens[0].isnumeric() or tokens[0].isupper():
            fmt = [PRE, SUF, NULL]
        elif tokens[1].islower():
            fmt = [FAM, SUF, NULL]
        elif len(tokens[1]) >= 5:
            fmt = [FAM, FAM, NULL]
        else:
            fmt = [FAM, SUF, NULL]
        return fmt
