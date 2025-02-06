import re
from claravy.taxonomy import *


class Parse_Alyac: # Based on Alyac, Sophos, and Tera engine

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK:TOK.TOK.TOK": self.parse_delim_fmt3,
            "TOK:TOK.TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK!.TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK.TOK": self.parse_delim_fmt7,
            "TOK:TOK.TOK.TOK@TOK": self.parse_delim_fmt8,
            "TOK.TOK.TOK@TOK": self.parse_delim_fmt9,
            "TOK:TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt10,
            "TOK:TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt11,
            "TOK.TOK.TOK!TOK!TOK.TOK": self.parse_delim_fmt12,
            "TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt13,
            "TOK:TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt14,
            "TOK.TOK-TOK.TOK": self.parse_delim_fmt15,
            "TOK.TOK-TOK-TOK.TOK": self.parse_delim_fmt16,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt17,
            "TOK:TOK.TOK.TOK@TOK@TOK": self.parse_delim_fmt18,
            "TOK.TOK.TOK!TOK!.TOK": self.parse_delim_fmt19,
            "TOK:TOK.TOK.TOK@TOK!TOK": self.parse_delim_fmt20,
            "TOK.TOK.TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt21,
            "TOK.TOK-TOK": self.parse_delim_fmt22,
            "TOK:TOK.TOK.TOK.@TOK@TOK": self.parse_delim_fmt23,
            "TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt24,
            "TOK.TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt25,
            "TOK:TOK.TOK-TOK.TOK@TOK": self.parse_delim_fmt26,
            "TOK:TOK.TOK.TOK!TOK!TOK.TOK": self.parse_delim_fmt27,
            "TOK:TOK.TOK.TOK!TOK!.TOK": self.parse_delim_fmt28,
            "TOK.TOK.TOK!!.TOK": self.parse_delim_fmt29,
            "TOK:TOK.TOK.TOK!.TOK": self.parse_delim_fmt30,
            "TOK:TOK.TOK-TOK.TOK": self.parse_delim_fmt31,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt32,
            "TOK:TOK.TOK": self.parse_delim_fmt33,
            "TOK.TOK.TOK.TOK (TOK TOK)": self.parse_delim_fmt34,
            "TOK:TOK.TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt35,
            "TOK:TOK.TOK.TOK.@TOK": self.parse_delim_fmt36,
            "TOK:TOK.TOK.TOK!TOK": self.parse_delim_fmt37,
            "TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt38,
            "TOK:TOK.TOK.TOK.TOK@TOK@TOK": self.parse_delim_fmt39,
            "TOK:TOK.TOK.TOK.TOK@TOK!TOK": self.parse_delim_fmt40,
            "TOK.TOK.TOK.TOK.TOK@TOK": self.parse_delim_fmt41,
            "TOK:TOK.TOK.TOK!!.TOK": self.parse_delim_fmt42,
            "TOK.TOK.TOK-TOK-TOK.TOK": self.parse_delim_fmt43,
            "TOK:TOK.TOK@TOK": self.parse_delim_fmt44,
        }


    # TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [NULL, NULL, NULL]
        if tokens[2].isnumeric():
            tax = [PRE, FAM, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[2]):
            tax = [PRE, FAM, SUF]
        elif tokens[1].isnumeric():
            tax = [FAM, SUF, SUF]
        elif len(tokens[2]) <= 3 or (len(tokens[2]) == 4 and tokens[2].isupper()):
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        tax = [NULL, NULL, NULL, NULL]
        if tokens[0] == "Packer":
            tax = [PRE, PRE, PACK, SUF]
        elif tokens[3].isnumeric():
            if tokens[2] in ["Gen", "GenericKD"] or len(tokens[2]) <= 2:
                tax = [PRE, FAM, SUF, SUF]
            elif tokens[2].isupper() and len(tokens[2]) <= 3:
                tax = [PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        else:
            if len(tokens[2]) <= 3 and tokens[2] != "VB":
                tax = [PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK:TOK.TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK!.TOK
    def parse_delim_fmt5(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        if re.match(r"[0-9A-F]{8}", tokens[4]):
            if tokens[3].isnumeric():
                tax = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[3].isupper() and len(tokens[3]) <= 3:
                tax = [PRE, PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF]
        elif tokens[2] == "CVE":
            tax = [PRE, PRE, VULN, VULN, VULN]
        elif re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF]
        elif "plugin" in [tokens[2].lower(), tokens[3].lower(), tokens[4].lower()]:
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].isnumeric() or tokens[3] == "Gen":
            if tokens[2].isnumeric() or tokens[2] in ["Dropper", "Based"]:
                tax = [PRE, FAM, SUF, SUF, SUF]
            elif len(tokens[2]) <= 2 and tokens[2] != "VB":
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[2].isnumeric():
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].islower():
            tax = [PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[3]) == 2:
            if re.match(r"V[0-9]", tokens[3]):
                tax = [PRE, PRE, FAM, SUF, SUF]
            elif tokens[1].lower() == "aol":
                tax = [PRE, PRE, PRE, SUF, SUF]
            elif tokens[3].lower() == "vb":
                tax = [PRE, PRE, PRE, PRE, SUF]
            elif tokens[2] == "VB":
                tax = [PRE, PRE, FAM, SUF, SUF]
            elif len(tokens[2]) <= 3:
                tax = [PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF]
        elif tokens[4].isnumeric():
            if len(tokens[3]) <= 3:
                if len(tokens[2]) <= 3:
                    tax = [PRE, FAM, SUF, SUF, SUF]
                else:
                    tax = [PRE, PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK.TOK
    def parse_delim_fmt7(self, tokens):
        if tokens[1].isnumeric() or len(tokens[1]) <= 2:
            tax = [FAM, SUF]
        elif len(tokens[1]) == 3: # Some families with names that are all caps, 3 letters
            tax = [PRE, UNK]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK:TOK.TOK.TOK@TOK
    def parse_delim_fmt8(self, tokens):
        if tokens[2] == "Heur":
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK@TOK
    def parse_delim_fmt9(self, tokens):
        return [FILE, FAM, SUF, SUF]

    # TOK:TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt10(self, tokens):
        tax = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[4].isnumeric() or len(tokens[4]) == 1:
            if tokens[3].isnumeric() or len(tokens[3]) == 1:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if (tokens[4].isupper() and tokens[4] != "VB") or tokens[4] == "Gen":
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt11(self, tokens):
        tax = [PRE, PRE, NULL, NULL, NULL, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF]
        elif len(tokens[4]) <= 3:
            if len(tokens[3]) <= 3:
                if tokens[2].startswith("Heur"):
                    tax = [PRE, PRE, PRE, SUF, SUF, SUF]
                else:
                    tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            elif tokens[3].startswith("Heur"):
                tax = [PRE, PRE, PRE, PRE, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        else:
            if tokens[3].isupper() and len(tokens[3]) <= 3:
                tax = [PRE, PRE, PRE, SUF, SUF, SUF]
            elif tokens[3].startswith("Heur"):
                tax = [PRE, PRE, PRE, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK!TOK!TOK.TOK
    def parse_delim_fmt12(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt13(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt14(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK-TOK.TOK
    def parse_delim_fmt15(self, tokens):
        if re.match(r"M[Ss][0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN, SUF]
        elif len(tokens[3]) > 3:
            if tokens[3].isnumeric():
                tax = [PRE, FAM, FAM, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM]
        elif len(tokens[1]) <= 3 and len(tokens[2]) <= 3:
            if tokens[3].isnumeric():
                tax = [FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, SUF]
        elif tokens[3].isnumeric(): # Not sure how to distinguish, few examples
            tax = [UNK, UNK, UNK, SUF]
        elif tokens[2].isnumeric():
            if tokens[0] == "Exploit":
                tax = [PRE, VULN, SUF, SUF]
            else:
                tax = [PRE, FAM, SUF, SUF]
        else:
            if tokens[0] == "Exploit":
                tax = [PRE, PRE, PRE, SUF]
            else:
                tax = [PRE, FAM, FAM, SUF]
        return tax

    # TOK.TOK-TOK-TOK.TOK
    def parse_delim_fmt16(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if tokens[1] == "CVE" and tokens[2].isnumeric() and tokens[3].isnumeric():
            tax = [PRE, VULN, VULN, VULN, SUF]
        else:
            tax = [PRE, PRE, PRE, PRE, SUF]
        return tax

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt17(self, tokens):
        return [FAM, FAM, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK@TOK@TOK
    def parse_delim_fmt18(self, tokens):
        if tokens[2].startswith("Heur"):
            tax = [PRE, PRE, PRE, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        return tax

    # TOK.TOK.TOK!TOK!.TOK
    def parse_delim_fmt19(self, tokens):
        return [PRE, PRE, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK@TOK!TOK
    def parse_delim_fmt20(self, tokens):
        return self.parse_delim_fmt18(tokens)

    # TOK.TOK.TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt21(self, tokens):
        tax = [PRE, UNK, UNK, UNK, UNK, SUF]
        if re.match(r"[0-9A-F]{8}", tokens[5]):
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        elif tokens[3].lower() in ["cve", "can"] and tokens[4].isnumeric() and tokens[5].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[6]):
            tax = [PRE, PRE, PRE, PRE, FAM, SUF, SUF]
        elif len(tokens[4]) <= 2 and len(tokens[5]) <= 2 and len(tokens[6]) <= 2:
            if len(tokens[3]) <= 2:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        else: # Some unusual multi-token family names left over
            tax = [PRE, UNK, UNK, UNK, UNK, UNK, SUF]
        return tax

    # TOK.TOK-TOK
    def parse_delim_fmt22(self, tokens):
        tax = [PRE, UNK, UNK]
        if re.match(r"M[Ss][0-9]{2}", tokens[1]) and tokens[2].isnumeric():
            tax = [PRE, VULN, VULN]
        elif tokens[2].isupper() or tokens[2].islower() or tokens[2].isnumeric():
            if len(tokens[1]) <= 3:
                if tokens[1] == "PS" and tokens[2] == "MPC":
                    tax = [PRE, FAM, FAM]
                else: # Remaining labels don't appear to contain families, but unsure
                    tax = [PRE, UNK, UNK]
            else:
                tax = [PRE, FAM, SUF]
        elif tokens[2].lower() in ["gen", "fam"]:
            tax = [PRE, FAM, SUF]
        else:
            tax = [PRE, FAM, FAM]
        return tax

    # TOK:TOK.TOK.TOK.@TOK@TOK
    def parse_delim_fmt23(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF]
        if len(tokens[3]) <= 3:
            tax = [PRE, PRE, PRE, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt24(self, tokens):
        tax = [PRE, UNK, UNK, SUF, SUF]
        if tokens[2] == "Gen":
            tax = [PRE, FAM, SUF, SUF, SUF]
        elif len(tokens[2]) <= 2 and tokens[2] != "VB":
            tax = [PRE, FAM, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, FAM, SUF, SUF]
        return tax

    # TOK.TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt25(self, tokens):
        tax = [PRE, UNK, UNK, UNK, UNK, SUF]
        if tokens[3].lower() in ["cve", "can"] and tokens[4].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif tokens[2].lower() in ["cve", "can"] and tokens[3].isnumeric() and tokens[4].isnumeric():
            tax = [PRE, PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"M[Ss][0-9]{2}", tokens[3]) and tokens[4].isnumeric():
            tax = [PRE, PRE, PRE, VULN, VULN, SUF]
        elif len(tokens[3]) <= 2 or tokens[3].isnumeric():
            if len(tokens[2]) <= 2 or tokens[2].isnumeric():
                if len(tokens[1]) <= 3:
                    tax = [PRE, PRE, SUF, SUF, SUF, SUF]
                else:
                    tax = [PRE, FAM, SUF, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[5]):
            tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        elif tokens[4].isnumeric() or len(tokens[4]) <= 2:
            if tokens[3] in ["Beta", "RAT"]:
                tax = [PRE, PRE, FAM, SUF, SUF, SUF]
            else:
                tax = [PRE, PRE, PRE, FAM, SUF, SUF]
        else: # Rest of AV labels have no clear pattern
            tax = [PRE, PRE, UNK, UNK, UNK, SUF]
        return tax

    # TOK:TOK.TOK-TOK.TOK@TOK
    def parse_delim_fmt26(self, tokens):
        return [PRE, PRE, CAT, CAT, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK!TOK.TOK
    def parse_delim_fmt27(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF, SUF]

    # TOK:TOK.TOK.TOK!TOK!.TOK
    def parse_delim_fmt28(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF, SUF]

    # TOK.TOK.TOK!!.TOK
    def parse_delim_fmt29(self, tokens):
        return [PRE, PRE, SUF, SUF]

    # TOK:TOK.TOK.TOK!.TOK
    def parse_delim_fmt30(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]

    # TOK:TOK.TOK-TOK.TOK
    def parse_delim_fmt31(self, tokens):
        return [PRE, PRE, CAT, CAT, SUF]

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt32(self, tokens):
        if tokens[3].isnumeric() or len(tokens[3]) == 1:
            if tokens[2].isnumeric():
                tax = [FAM, FAM, SUF, SUF]
            else:
                tax = [PRE, PRE, FAM, SUF]
        else: # A few remaining labels with no predictable pattern
            tax = [UNK, UNK, UNK, SUF]
        return tax

    # TOK:TOK.TOK
    def parse_delim_fmt33(self, tokens):
        if tokens[2].isnumeric():
            if tokens[0] == "VBA" or len(tokens[2]) <= 2:
                tax = [PRE, FAM, SUF]
            else: # Second token mostly CAT, but rarely FAM
                tax = [PRE, UNK, SUF]
        else:
            tax = [PRE, PRE, FAM]
        return tax

    # TOK.TOK.TOK.TOK (TOK TOK)
    def parse_delim_fmt34(self, tokens):
        tax = [UNK, UNK, UNK, SUF, SUF, SUF, NULL]
        if tokens[0] != "Stoned": # Skip rare prefix with unusual family name format
            tax = [CAT, PRE, FAM, SUF, SUF, SUF, NULL]
        return tax

    # TOK:TOK.TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt35(self, tokens):
        tax = [PRE, PRE, PRE, UNK, SUF, SUF, SUF]
        if len(tokens[3]) <= 2:
            tax = [PRE, PRE, PRE, SUF, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        return tax

    # TOK:TOK.TOK.TOK.@TOK
    def parse_delim_fmt36(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF]
        elif len(tokens[3]) <= 2:
            tax = [PRE, PRE, PRE, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF]
        return tax

    # TOK:TOK.TOK.TOK!TOK
    def parse_delim_fmt37(self, tokens):
        tax = [PRE, PRE, UNK, SUF, SUF]
        if tokens[2].startswith("Heur"):
            tax = [PRE, PRE, PRE, SUF, SUF]
        elif tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF]
        else:
            tax = [PRE, PRE, CAT, SUF, SUF]
        return tax

    # TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt38(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF]
        if re.match(r"M[Ss][0-9]{2}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF]
        elif re.match(r"[Cc][Vv][Ee][0-9]{4}", tokens[2]) and tokens[3].isnumeric():
            tax = [PRE, PRE, VULN, VULN, SUF]
        elif tokens[1].lower() == "cve" and tokens[2].isnumeric() and tokens[3].isnumeric():
            tax = [PRE, VULN, VULN, VULN, SUF]
        elif re.match(r"[0-9A-F]{8}", tokens[4]):
            tax = [PRE, PRE, PRE, PRE, SUF]
        elif tokens[0] == "Trojan":
            tax = [PRE, PRE, FAM, FAM, SUF]
        else: # Does not seem to contain any families, unclear how to parse
            tax = [PRE, UNK, UNK, SUF, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK@TOK
    def parse_delim_fmt39(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF, SUF, SUF]
        if tokens[1] == "Packer":
            tax = [PRE, PRE, PACK, SUF, SUF, SUF, SUF]
        elif len(tokens[3]) <= 3 and (tokens[3].isupper() or tokens[3].isnumeric()):
            tax = [PRE, PRE, PRE, SUF, SUF, SUF, SUF]
        elif tokens[3].startswith("Heur"):
            tax = [PRE, PRE, PRE, PRE, SUF, SUF, SUF]
        else:
            tax = [PRE, PRE, PRE, FAM, SUF, SUF, SUF]
        return tax

    # TOK:TOK.TOK.TOK.TOK@TOK!TOK
    def parse_delim_fmt40(self, tokens):
        return self.parse_delim_fmt39(tokens)

    # TOK.TOK.TOK.TOK.TOK@TOK
    def parse_delim_fmt41(self, tokens):
        tax = [PRE, UNK, UNK, UNK, SUF, SUF]
        if tokens[3] == "Gen":
            tax = [PRE, PRE, FAM, SUF, SUF, SUF]
        # A few tokens left over with no predictable structure
        return tax

    # TOK:TOK.TOK.TOK!!.TOK
    def parse_delim_fmt42(self, tokens):
        return [PRE, PRE, PRE, SUF, SUF]

    # TOK.TOK.TOK-TOK-TOK.TOK
    def parse_delim_fmt43(self, tokens):
        return [PRE, PRE, VULN, VULN, VULN, SUF]

    # TOK:TOK.TOK@TOK
    def parse_delim_fmt44(self, tokens):
        return [PRE, PRE, SUF, SUF]
