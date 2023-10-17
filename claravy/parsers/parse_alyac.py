import re
from claravy.taxonomy import *


class Parse_Alyac: # Based on Alyac, Sophos, and Tera engine

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK!.TOK": self.parse_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt6,
            "TOK.TOK": self.parse_fmt7,
            "TOK:TOK.TOK.TOK@TOK": self.parse_fmt8,
            "TOK.TOK.TOK@TOK": self.parse_fmt9,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_fmt10,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_fmt11,
            "TOK.TOK.TOK!TOK!TOK.TOK": self.parse_fmt12,
            "TOK.TOK.TOK!TOK.TOK": self.parse_fmt13,
            "TOK:TOK.TOK.TOK!TOK.TOK": self.parse_fmt14,
            "TOK.TOK-TOK.TOK": self.parse_fmt15,
            "TOK.TOK-TOK-TOK.TOK": self.parse_fmt16,
            "TOK-TOK.TOK.TOK.TOK": self.parse_fmt17,
            "TOK:TOK.TOK.TOK@TOK@TOK": self.parse_fmt18,
            "TOK.TOK.TOK!TOK!.TOK": self.parse_fmt19,
            "TOK:TOK.TOK.TOK@TOK!TOK": self.parse_fmt20,
            "TOK.TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt21,
            "TOK.TOK-TOK": self.parse_fmt22,
            "TOK:TOK.TOK.TOK.@TOK@TOK": self.parse_fmt23,
            "TOK.TOK.TOK.TOK@TOK": self.parse_fmt24,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_fmt25,
            "TOK:TOK.TOK-TOK.TOK@TOK": self.parse_fmt26,
            "TOK:TOK.TOK.TOK!TOK!TOK.TOK": self.parse_fmt27,
            "TOK:TOK.TOK.TOK!TOK!.TOK": self.parse_fmt28,
            "TOK.TOK.TOK!!.TOK": self.parse_fmt29,
            "TOK:TOK.TOK.TOK!.TOK": self.parse_fmt30,
            "TOK:TOK.TOK-TOK.TOK": self.parse_fmt31,
            "TOK-TOK.TOK.TOK": self.parse_fmt32,
            "TOK:TOK.TOK": self.parse_fmt33,
            "TOK.TOK.TOK.TOK (TOK TOK)": self.parse_fmt34,
            "TOK:TOK.TOK.TOK.TOK.TOK@TOK": self.parse_fmt35,
            "TOK:TOK.TOK.TOK.@TOK": self.parse_fmt36,
            "TOK:TOK.TOK.TOK!TOK": self.parse_fmt37,
            "TOK.TOK.TOK-TOK.TOK": self.parse_fmt38,
            "TOK:TOK.TOK.TOK.TOK@TOK@TOK": self.parse_fmt39,
            "TOK:TOK.TOK.TOK.TOK@TOK!TOK": self.parse_fmt40,
            "TOK.TOK.TOK.TOK.TOK@TOK": self.parse_fmt41,
            "TOK:TOK.TOK.TOK!!.TOK": self.parse_fmt42,
            "TOK.TOK.TOK-TOK-TOK.TOK": self.parse_fmt43,
            "TOK:TOK.TOK@TOK": self.parse_fmt44,
        }


    # TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [NULL, NULL, NULL]
        if tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[2]):
            fmt = [PRE, FAM, SUF]
        elif tokens[1].isnumeric():
            fmt = [FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 or (len(tokens[2]) == 4 and tokens[2].isupper()):
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK
    def parse_fmt2(self, tokens):
        fmt = [NULL, NULL, NULL, NULL]
        if tokens[0] == "Packer":
            fmt = [PRE, PRE, PACK, SUF]
        elif tokens[3].isnumeric():
            if tokens[2] in ["Gen", "GenericKD"] or len(tokens[2]) <= 2:
                fmt = [PRE, FAM, SUF, SUF]
            elif tokens[2].isupper() and len(tokens[2]) <= 3:
                fmt = [PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        else:
            if len(tokens[2]) <= 3 and tokens[2] != "VB":
                fmt = [PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK
    def parse_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK!.TOK
    def parse_fmt5(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt6(self, tokens):
        if re.match(r"[0-9A-F]{8}", tokens[4]):
            if tokens[3].isnumeric():
                fmt = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[3].isupper() and len(tokens[3]) <= 3:
                fmt = [PRE, PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF]
        elif tokens[2] == "CVE":
            fmt = [PRE, PRE, VULN, VULN, VULN]
        elif re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, SUF]
        elif "plugin" in [tokens[2].lower(), tokens[3].lower(), tokens[4].lower()]:
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            if tokens[2].isnumeric() or tokens[2] in ["Dropper", "Based"]:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            elif len(tokens[2]) <= 2 and tokens[2] != "VB":
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].islower():
            fmt = [PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[3]) == 2:
            if re.match(r"V[0-9]", tokens[3]):
                fmt = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[1].lower() == "aol":
                fmt = [PRE, PRE, PRE, SUF, SUF]
            elif tokens[3].lower() == "vb":
                fmt = [PRE, PRE, PRE, PRE, SUF]
            elif tokens[2] == "VB":
                fmt = [PRE, PRE, FAM, SUF, SUF]
            elif len(tokens[2]) <= 3:
                fmt = [PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[4].isnumeric():
            if len(tokens[3]) <= 3:
                if len(tokens[2]) <= 3:
                    fmt = [PRE, FAM, SUF, SUF, SUF]
                else:
                    fmt = [PRE, PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK.TOK
    def parse_fmt7(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) <= 2:
            fmt = [FAM, SUF]
        elif len(tokens[1]) == 3: # Some families with names that are all caps, 3 letters
            fmt = [PRE, UNK]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK:TOK.TOK.TOK@TOK
    def parse_fmt8(self, tokens):
        if tokens[2] == "Heur":
            fmt = [PRE, PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK@TOK
    def parse_fmt9(self, tokens):
        return [TGT, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_fmt10(self, tokens):
        fmt = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[4].isnumeric() or len(tokens[4]) == 1:
            if tokens[3].isnumeric() or len(tokens[3]) == 1:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if (tokens[4].isupper() and tokens[4] != "VB") or tokens[4] == "Gen":
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, PRE, FAM, SUF]
        else:
            fmt = [PRE, PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_fmt11(self, tokens):
        fmt = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if len(tokens[3]) <= 3:
                if tokens[2].startswith("Heur"):
                    fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
                else:
                    fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
            elif tokens[3].startswith("Heur"):
                fmt = [PRE, PRE, PRE, PRE, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        else:
            if tokens[3].isupper() and len(tokens[3]) <= 3:
                fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
            elif tokens[3].startswith("Heur"):
                fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK!TOK!TOK.TOK
    def parse_fmt12(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_fmt13(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK.TOK
    def parse_fmt14(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK-TOK.TOK
    def parse_fmt15(self, tokens):
        if re.match(r"M[Ss][0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN, SUF]
        elif len(tokens[3]) > 3:
            if tokens[3].isnumeric():
                fmt = [PRE, FAM, FAM, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM]
        elif len(tokens[1]) <= 3 and len(tokens[2]) <= 3:
            if tokens[3].isnumeric():
                fmt = [FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, SUF]
        elif tokens[3].isnumeric(): # Not sure how to distinguish, few examples
            fmt = [UNK, UNK, UNK, SUF]
        elif tokens[2].isnumeric():
            if tokens[0] == "Exploit":
                fmt = [PRE, VULN, SUF, SUF]
            else:
                fmt = [PRE, FAM, SUF, SUF]
        else:
            if tokens[0] == "Exploit":
                fmt = [PRE, PRE, PRE, SUF]
            else:
                fmt = [PRE, FAM, FAM, SUF]
        return fmt

    # TOK.TOK-TOK-TOK.TOK
    def parse_fmt16(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "CVE" and tokens[2].isnumeric() and tokens[3].isnumeric():
            fmt = [PRE, VULN, VULN, VULN, SUF]
        else:
            fmt = [PRE, PRE, PRE, PRE, SUF]
        return fmt

    # TOK-TOK.TOK.TOK.TOK
    def parse_fmt17(self, tokens):
        return [FAM, FAM, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK@TOK@TOK
    def parse_fmt18(self, tokens):
        if tokens[2].startswith("Heur"):
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        return fmt

    # TOK.TOK.TOK!TOK!.TOK
    def parse_fmt19(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK@TOK!TOK
    def parse_fmt20(self, tokens):
        return self.parse_fmt18(tokens)

    # TOK.TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt21(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, UNK, SUF]
        if re.match(r"[0-9A-F]{8}", tokens[5]):
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].lower() in ["cve", "can"] and tokens[4].isnumeric() and tokens[5].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[6]):
            fmt = [PRE, PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 2 and len(tokens[5]) <= 2 and len(tokens[6]) <= 2:
            if len(tokens[3]) <= 2:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        else: # Some unusual multi-token family names left over
            fmt = [PRE, UNK, UNK, UNK, UNK, UNK, SUF]
        return fmt

    # TOK.TOK-TOK
    def parse_fmt22(self, tokens):
        fmt = [PRE, UNK, UNK]
        if re.match(r"M[Ss][0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            fmt = [PRE, VULN, VULN]
        elif tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric():
            if len(tokens[1]) <= 3:
                if tokens[1] == "PS" and tokens[2] == "MPC":
                    fmt = [PRE, FAM, FAM]
                else: # Remaining labels don't appear to contain families, but unsure
                    fmt = [PRE, UNK, UNK]
            else:
                fmt = [PRE, FAM, SUF]
        elif tokens[2].lower() in ["gen", "fam"]:
            fmt = [PRE, FAM, SUF]
        else:
            fmt = [PRE, FAM, FAM]
        return fmt

    # TOK:TOK.TOK.TOK.@TOK@TOK
    def parse_fmt23(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF]
        if len(tokens[3]) <= 3:
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK.TOK@TOK
    def parse_fmt24(self, tokens):
        fmt = [PRE, UNK, UNK, SUF, SUF]
        if tokens[2] == "Gen":
            fmt = [PRE, FAM, SUF, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            fmt = [PRE, FAM, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, FAM, SUF, SUF]
        return fmt

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_fmt25(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, UNK, SUF]
        if tokens[3].lower() in ["cve", "can"] and tokens[4].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif tokens[2].lower() in ["cve", "can"] and tokens[3].isnumeric() and tokens[4].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            fmt = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric():
            if len(tokens[2]) <= 2 or tokens[2].isnumeric():
                if len(tokens[1]) <= 3:
                    fmt = [PRE, PRE, SUF, SUF, SUF, SUF]
                else:
                    fmt = [PRE, FAM, SUF, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[5]):
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif tokens[4].isnumeric() or len(tokens[4]) <= 2:
            if tokens[3] in ["Beta", "RAT"]:
                fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                fmt = [PRE, PRE, PRE, FAM, SUF, SUF]
        else: # Rest of AV labels have no clear pattern
            fmt = [PRE, PRE, UNK, UNK, UNK, SUF]
        return fmt

    # TOK:TOK.TOK-TOK.TOK@TOK
    def parse_fmt26(self, tokens):
        return [PRE, PRE, CAT, CAT, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK!TOK.TOK
    def parse_fmt27(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK!.TOK
    def parse_fmt28(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK.TOK!!.TOK
    def parse_fmt29(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK:TOK.TOK.TOK!.TOK
    def parse_fmt30(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]

    # TOK:TOK.TOK-TOK.TOK
    def parse_fmt31(self, tokens):
        return [PRE, PRE, CAT, CAT, SUF]

    # TOK-TOK.TOK.TOK
    def parse_fmt32(self, tokens):
        if tokens[3].isnumeric() or len(tokens[3]) == 1:
            if tokens[2].isnumeric():
                fmt = [FAM, FAM, SUF, SUF]
            else:
                fmt = [PRE, PRE, FAM, SUF]
        else: # A few remaining labels with no predictable pattern
            fmt = [UNK, UNK, UNK, SUF]
        return fmt

    # TOK:TOK.TOK
    def parse_fmt33(self, tokens):
        if tokens[2].isnumeric():
            if tokens[0] == "VBA" or len(tokens[2]) <= 2:
                fmt = [PRE, FAM, SUF]
            else: # Second token mostly CAT, but rarely FAM
                fmt = [PRE, UNK, SUF]
        else:
            fmt = [PRE, PRE, FAM]
        return fmt

    # TOK.TOK.TOK.TOK (TOK TOK)
    def parse_fmt34(self, tokens):
        fmt = [UNK, UNK, UNK, SUF, SUF, SUF, NULL]
        if tokens[0] != "Stoned": # Skip rare prefix with unusual family name format
            fmt = [CAT, PRE, FAM, SUF, SUF, SUF, NULL]
        return fmt

    # TOK:TOK.TOK.TOK.TOK.TOK@TOK
    def parse_fmt35(self, tokens):
        fmt = [PRE, PRE, PRE, UNK, SUF, SUF, SUF]
        if len(tokens[3]) <= 2:
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.@TOK
    def parse_fmt36(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF]
        elif len(tokens[3]) <= 2:
            fmt = [PRE, PRE, PRE, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF]
        return fmt

    # TOK:TOK.TOK.TOK!TOK
    def parse_fmt37(self, tokens):
        fmt = [PRE, PRE, UNK, SUF, SUF]
        if tokens[2].startswith("Heur"):
            fmt = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF]
        else:
            fmt = [PRE, PRE, CAT, SUF, SUF]
        return fmt

    # TOK.TOK.TOK-TOK.TOK
    def parse_fmt38(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF]
        if re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, SUF]
        elif re.match(r"[Cc][Vv][Ee][0-9]{4}", tokens[2]) and tokens[3].isnumeric():
            fmt = [PRE, PRE, VULN, VULN, SUF]
        elif tokens[1].lower() == "cve" and tokens[2].isnumeric() and tokens[3].isnumeric():
            fmt = [PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[4]):
            fmt = [PRE, PRE, PRE, PRE, SUF]
        elif tokens[0] == "Trojan":
            fmt = [PRE, PRE, FAM, FAM, SUF]
        else: # Does not seem to contain any families, unclear how to parse
            fmt = [PRE, UNK, UNK, SUF, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK@TOK@TOK
    def parse_fmt39(self, tokens):
        fmt = [PRE, PRE, UNK, UNK, SUF, SUF, SUF]
        if tokens[1] == "Packer":
            fmt = [PRE, PRE, PACK, SUF, SUF, SUF, SUF]
        elif len(tokens[3]) <= 3 and (tokens[3].isupper() or tokens[3].isnumeric()):
            fmt = [PRE, PRE, PRE, SUF, SUF, SUF, SUF]
        elif tokens[3].startswith("Heur"):
            fmt = [PRE, PRE, PRE, PRE, SUF, SUF, SUF]
        else:
            fmt = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        return fmt

    # TOK:TOK.TOK.TOK.TOK@TOK!TOK
    def parse_fmt40(self, tokens):
        return self.parse_fmt39(tokens)

    # TOK.TOK.TOK.TOK.TOK@TOK
    def parse_fmt41(self, tokens):
        fmt = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[3] == "Gen":
            fmt = [PRE, PRE, FAM, SUF, SUF, SUF]
        # A few tokens left over with no predictable structure
        return fmt

    # TOK:TOK.TOK.TOK!!.TOK
    def parse_fmt42(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]

    # TOK.TOK.TOK-TOK-TOK.TOK
    def parse_fmt43(self, tokens):
        return [PRE, PRE, VULN, VULN, VULN, SUF]

    # TOK:TOK.TOK@TOK
    def parse_fmt44(self, tokens):
        return [PRE, PRE, SUF, SUF]
