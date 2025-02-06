import re
from claravy.taxonomy import *


class Parse_Antivir: # Renamed to Avira. Format similar to Thehacker but does not seem related.

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK/TOK.TOK": self.parse_delim_fmt1,
            "TOK/TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK/TOK.TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK/TOK": self.parse_delim_fmt4,
            "TOK/TOK-TOK-TOK.TOK": self.parse_delim_fmt5,
            "TOK/TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK #TOK": self.parse_delim_fmt7,
            "TOK-TOK": self.parse_delim_fmt8,
            "TOK": self.parse_delim_fmt9,
            "TOK/TOK-TOK.TOK": self.parse_delim_fmt10,
            "TOK_#TOK": self.parse_delim_fmt11,
            "TOK/TOK.#TOK": self.parse_delim_fmt12,
            "TOK.TOK": self.parse_delim_fmt13,
            "TOK-TOK-TOK #TOK": self.parse_delim_fmt14,
            "TOK-TOK (TOK)": self.parse_delim_fmt15,
            "TOK/TOK-TOK.TOK.TOK": self.parse_delim_fmt16,
            "TOK/TOK-TOK": self.parse_delim_fmt17,
            "TOK/TOK.TOK-TOK": self.parse_delim_fmt18,
            "TOK (TOK) #TOK": self.parse_delim_fmt19,
            "TOK/TOK.TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt20,
            "_TOK_TOK_TOK": self.parse_delim_fmt21,
            "TOK (TOK)": self.parse_delim_fmt22,
        }


    # TOK/TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK]
        if len(tokens[2]) <= 4 or tokens[2][0].isnumeric() or tokens[2].islower():
            tax = [PRE, FAM, SUF]
        # A few remaining labels have unclear formats
        return tax

    # TOK/TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2].isnumeric() or tokens[2].islower():
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 and tokens[2].isupper():
            tax = [PRE, FAM, SUF, SUF]
        elif len(tokens[2]) <= 2:
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[1] == "Crypt":
            tax = [PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if len(tokens[3]) <= 4 or tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isnumeric() or tokens[2].islower():
                tax = [PRE, FAM, SUF, SUF, SUF]
            elif len(tokens[2]) <= 2 and tokens[2] != "VB":
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[3].isupper() or re.search(r"\d", tokens[3]):
            tax = [PRE, PRE, FAM, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK/TOK
    def parse_delim_fmt4(self, tokens):
        tax = [UNK, UNK]
        if tokens[0] == "PCK":
            tax = [PRE, PACK]
        elif tokens[1].isnumeric(): # First token is very rarely FAM, mostly PRE
            tax = [UNK, SUF]
        elif tokens[1].isupper() and (len(tokens[1]) <= 2 or not tokens[0].isupper()): # Another odd format
            tax = [UNK, UNK]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK/TOK-TOK-TOK.TOK
    def parse_delim_fmt5(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1].lower() in ["c", "cv", "cve", "can"] and tokens[2].isnumeric() and tokens[3].isnumeric():
            tax = [PRE, VULN, VULN, VULN, SUF]
        elif tokens[3].startswith("base"):
            tax = [PRE, FAM, FAM, SUF, SUF]
        # A few unusually formatted labels left over
        return tax

    # TOK/TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        tax = [PRE, UNK, UNK, UNK, UNK, SUF]
        if tokens[1].lower() in ["c", "cv", "cve", "can"] and tokens[2].isnumeric() and tokens[3].isnumeric():
            tax = [PRE, VULN, VULN, VULN, SUF, SUF]
        elif tokens[2].lower() in ["c", "cv", "cve", "can"] and tokens[3].isnumeric() and tokens[4].isnumeric():
            tax = [PRE, PRE, VULN, VULN, VULN, SUF]
        elif tokens[3].isnumeric() or tokens[3].islower():
            if tokens[2].isnumeric() or tokens[2].islower():
                tax = [PRE, FAM, SUF, SUF, SUF, SUF]
            elif tokens[2].isupper() or (len(tokens[2]) <= 2 and tokens[2] != "VB"): # Unusual format
                tax = [PRE, UNK, SUF, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isupper() or tokens[3] == "Gen":
            if len(tokens[2]) <= 2 and tokens[2] != "VB":
                tax = [PRE, CAT, PRE, SUF, SUF, SUF]
            else:
                tax = [PRE, CAT, FAM, SUF, SUF, SUF]
        elif len(tokens[2]) <= 1:
            tax = [PRE, FAM, SUF, SUF, SUF, SUF]
        else:
            tax = [CAT, CAT, PRE, FAM, SUF, SUF]
        return tax

    # TOK #TOK
    def parse_delim_fmt7(self, tokens):
        return [FAM, SUF]

    # TOK-TOK
    def parse_delim_fmt8(self, tokens):
        tax = [UNK, UNK]
        if tokens[0] == "Trivial":
            if tokens[1].isnumeric():
                tax = [PRE, SUF]
            else:
                tax = [PRE, FAM]
        elif tokens[1].isnumeric() or tokens[1] == "based":
            if len(tokens[0]) <= 2:
                tax = [UNK, SUF]
            else:
                tax = [FAM, SUF]
        elif tokens[1] in ["Related", "Generic", "Trojan", "Small"]:
            tax = [FAM, SUF]
        elif len(tokens[1]) <= 2 and tokens[1].isupper():
            tax = [FAM, SUF]
        elif tokens[0].isupper(): # Unusual label format
            tax = [UNK, UNK]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK 
    def parse_delim_fmt9(self, tokens):
        tax = [UNK]
        if tokens[0].isupper(): # Some FAM, some SUF
            tax = [UNK]
        elif tokens[0].isnumeric():
            tax = [SUF]
        else:
            tax = [FAM]
        return tax

    # TOK/TOK-TOK.TOK
    def parse_delim_fmt10(self, tokens):
        tax = [PRE, UNK, UNK, UNK]
        if tokens[2].islower() or tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF]
        elif tokens[0] == "EXP" and tokens[1].isnumeric() and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN, SUF]
        elif re.match(r"MS[0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN, SUF]
        elif tokens[1] == "BackDoor":
            tax = [PRE, CAT, SUF, SUF]
        elif tokens[0] in ["SPR", "DOS", "APPL"]:
            tax = [PRE, FAM, FAM, SUF]
        else: # TODO: Unsure how to parse remaining tokens
            tax = [PRE, UNK, UNK, UNK]
        return tax

    # TOK_#TOK
    def parse_delim_fmt11(self, tokens):
        return [FAM, SUF]

    # TOK_#TOK
    def parse_delim_fmt12(self, tokens):
        return [CAT, FAM, SUF]

    # TOK.TOK
    def parse_delim_fmt13(self, tokens):
        tax = [UNK, UNK]
        if len(tokens[1]) >= 3 and not tokens[1].isupper() and not tokens[1].isnumeric():
            if not tokens[0].isupper():
                if tokens[0] in ["Trivial", "Joke", "Stoned"]:
                    tax = [PRE, FAM]
                elif "Macro" in tokens[0]:
                    tax = [PRE, FAM]
                else:
                    tax = [FAM, FAM]
            else:
                tax = [PRE, FAM]
        elif tokens[1].isupper():
            tax = [UNK, SUF]
        else:
            tax = [FAM, SUF]
        return tax

    # TOK-TOK-TOK #TOK
    def parse_delim_fmt14(self, tokens):
        return [FAM, FAM, SUF, SUF]

    # TOK-TOK (TOK)
    def parse_delim_fmt15(self, tokens):
        tax = [UNK, UNK, SUF, NULL]
        if tokens[1].isnumeric():
            if tokens[0].isupper():
                tax = [UNK, SUF, SUF, NULL]
            else:
                tax = [FAM, SUF, SUF, NULL]
        elif tokens[0].isupper():
            tax = [UNK, UNK, SUF, NULL]
        else:
            tax = [FAM, FAM, SUF, SUF]
        return tax

    # TOK/TOK-TOK.TOK.TOK
    def parse_delim_fmt16(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[0] == "EXP" and tokens[1].isnumeric() and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN, SUF, SUF]
        elif re.match(r"MS[0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN, SUF, SUF]
        elif tokens[1] == "CVE": # Bad CVE format
            tax = [PRE, UNK, UNK, SUF, SUF]
        elif tokens[2].islower(): # Unclear format
            tax = [PRE, UNK, SUF, SUF, SUF]
        elif tokens[0] in ["SPR", "DOS", "APPL"]:
            if tokens[2].isnumeric(): # Unclear format
                tax = [PRE, UNK, UNK, SUF, SUF]
            else:
                tax = [PRE, FAM, FAM, SUF, SUF]
        elif not tokens[2].isupper() and not tokens[2].isnumeric():
            tax = [PRE, FAM, FAM, SUF, SUF]
        else:
            tax = [PRE, FAM, SUF, SUF, SUF]
        return tax

    # TOK/TOK-TOK
    def parse_delim_fmt17(self, tokens):
        if re.match(r"MS[0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN]
        elif len(tokens[2]) >= 3 and not tokens[2].isnumeric():
            if tokens[2].lower() == "based":
                tax = [PRE, FAM, SUF]
            elif tokens[0].isnumeric() and tokens[1].isnumeric(): # Very unusual format
                tax = [UNK, UNK, FAM]
            elif tokens[1] == "Trivial":
                tax = [PRE, PRE, SUF]
            else:
                tax = [PRE, FAM, FAM]
        else:
            tax = [PRE, FAM, SUF]
        return tax

    # TOK/TOK.TOK-TOK
    def parse_delim_fmt18(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if re.match(r"[Cc][Vv][Ee][0-9]{4}", tokens[2]):
            tax = [PRE, PRE, VULN, VULN]
        elif re.match(r"MS[0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN]
        # Remainer of labels do not contain families, unclear format
        return tax

    # TOK (TOK) #TOK
    def parse_delim_fmt19(self, tokens):
        return [FAM, SUF, SUF]

    # TOK/TOK.TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt20(self, tokens):
        tax = [PRE, UNK, UNK, UNK, UNK, UNK, SUF]
        if tokens[3].lower() == "cve" and tokens[4].isnumeric() and tokens[5].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"MS[0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, SUF, SUF]
        else: # Bad format, usually no FAM
            tax = [PRE, UNK, UNK, UNK, UNK, SUF, SUF]
        return tax

    # _TOK_TOK_TOK
    def parse_delim_fmt21(self, tokens):
        return [NULL, SUF, SUF, SUF]

    # TOK (TOK)
    def parse_delim_fmt22(self, tokens):
        tax = [UNK, UNK, NULL]
        if tokens[0].isnumeric() or tokens[0].isupper():
            tax = [PRE, SUF, NULL]
        elif tokens[1].islower():
            tax = [FAM, SUF, NULL]
        elif len(tokens[1]) >= 5:
            tax = [FAM, FAM, NULL]
        else:
            tax = [FAM, SUF, NULL]
        return tax
