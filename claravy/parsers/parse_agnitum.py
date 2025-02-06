from claravy.taxonomy import *


class Parse_Agnitum: # Acquired Virusbuster, Acquired by Yandex

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK!TOK": self.parse_delim_fmt2,
            "TOK/TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK!TOK": self.parse_delim_fmt5,
            "TOK.TOK!TOK/TOK": self.parse_delim_fmt6,
            "TOK.TOK!TOK++TOK": self.parse_delim_fmt7,
            "TOK.TOK.TOK!TOK/TOK+TOK": self.parse_delim_fmt8,
            "TOK.TOK!/TOK/TOK": self.parse_delim_fmt9,
            "TOK.TOK.TOK!TOK+TOK+TOK": self.parse_delim_fmt10,
            "TOK.TOK!TOK/+TOK": self.parse_delim_fmt11,
            "TOK.TOK.TOK.TOK!TOK": self.parse_delim_fmt12,
            "TOK.TOK!+TOK/TOK": self.parse_delim_fmt13,
            "TOK.TOK!+TOK+TOK": self.parse_delim_fmt14,
            "TOK.TOK!TOK//TOK": self.parse_delim_fmt15,
            "TOK.TOK!TOK+/TOK": self.parse_delim_fmt16,
            "TOK.TOK!/TOK+TOK": self.parse_delim_fmt17,
            "TOK_TOK.TOK": self.parse_delim_fmt18,
            "TOK/TOK-TOK": self.parse_delim_fmt19,
            "TOK.TOK-TOK!TOK": self.parse_delim_fmt20,
            "TOK.TOK-TOK-TOK": self.parse_delim_fmt21,
            "TOK-TOK": self.parse_delim_fmt22,
            "TOK.TOK!TOK++TOK+TOK": self.parse_delim_fmt23,
            "TOK-TOK.TOK": self.parse_delim_fmt24,
            "TOK_TOK.TOK.TOK": self.parse_delim_fmt25,
            "TOK/TOK.TOK": self.parse_delim_fmt26,
            "TOK.TOK.TOK!+TOK+TOK": self.parse_delim_fmt27,
            "TOK.TOK.TOK!TOK++TOK": self.parse_delim_fmt28,
            "TOK.TOK!": self.parse_delim_fmt29,
            "TOK.TOK!TOK+TOK": self.parse_delim_fmt30,
            "TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt31,
            "TOK.TOK.TOK!TOK/TOK": self.parse_delim_fmt32,
            "TOK.TOK.TOK!TOK+TOK": self.parse_delim_fmt33,
            "TOK.TOK.TOK.TOK.TOK": self.parse_delim_fmt34,
            "TOK!TOK": self.parse_delim_fmt35,
            "TOK.TOK!+TOK": self.parse_delim_fmt36,
            "TOK.TOK.TOK!": self.parse_delim_fmt37,
            "TOK.TOK": self.parse_delim_fmt38,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt39,
            "TOK.TOK!/TOK": self.parse_delim_fmt40,
            "TOK-TOK_TOK": self.parse_delim_fmt41,
            "TOK-TOK.TOK!TOK": self.parse_delim_fmt42,
            "TOK.TOK.TOK.TOK!TOK.TOK": self.parse_delim_fmt43,
            "TOK/TOK!TOK": self.parse_delim_fmt44,
            "TOK-TOK.TOK!TOK+TOK": self.parse_delim_fmt45,
            "TOK.TOK!TOK+TOK+TOK": self.parse_delim_fmt46,
            "TOK.TOK!TOK/TOK/TOK": self.parse_delim_fmt47,
            "TOK.TOK.TOK!+TOK": self.parse_delim_fmt48,
            "TOK.TOK!TOK/TOK+TOK": self.parse_delim_fmt49,
            "TOK.TOK!TOK+TOK/TOK": self.parse_delim_fmt50,
            "TOK": self.parse_delim_fmt51,
            "TOK.TOK.TOK!/TOK": self.parse_delim_fmt52,
            "TOK.TOK.TOK!TOK/TOK/TOK": self.parse_delim_fmt53,
            "TOK.TOK.TOK!TOK+TOK/TOK": self.parse_delim_fmt54
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        tax = [PRE, UNK, UNK, SUF]
        if tokens[2] == "Gen" or (tokens[2].isupper() and len(tokens[2]) <= 2):
            tax[1] = FAM
            tax[2] = SUF
        else:
            tax[1] = PRE
            tax[2] = FAM
        return tax

    # TOK.TOK!TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT, FAM, SUF]

    # TOK/TOK
    def parse_delim_fmt3(self, tokens):
        return [PRE, PACK]

    # TOK.TOK.TOK
    def parse_delim_fmt4(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK!TOK
    def parse_delim_fmt5(self, tokens):
        tax = [CAT, CAT, FAM, SUF]
        if tokens[2] == "Gen":
            tax = [CAT, FAM, SUF, SUF]
        return tax

    # TOK.TOK!TOK/TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK++TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK/TOK+TOK
    def parse_delim_fmt8(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!/TOK/TOK
    def parse_delim_fmt9(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK+TOK+TOK
    def parse_delim_fmt10(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!TOK/+TOK
    def parse_delim_fmt11(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK!TOK
    def parse_delim_fmt12(self, tokens):
        tax = [CAT, UNK, UNK, UNK, SUF]
        if tokens[1].isupper() and len(tokens[1]) <= 3:
            if tokens[2].isupper() and len(tokens[2]) <= 3:
                tax = [CAT, CAT, PRE, FAM, SUF]
            else:
                tax = [CAT, CAT, FAM, SUF, SUF]
        else:
            tax = [CAT, FAM, SUF, SUF, SUF]
        return tax

    # TOK.TOK!+TOK/TOK
    def parse_delim_fmt13(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!+TOK+TOK
    def parse_delim_fmt14(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK//TOK
    def parse_delim_fmt15(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK+/TOK
    def parse_delim_fmt16(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!/TOK+TOK
    def parse_delim_fmt17(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK_TOK.TOK
    def parse_delim_fmt18(self, tokens):
        return [FAM, FAM, SUF]

    # TOK/TOK-TOK
    def parse_delim_fmt19(self, tokens): # Unusual packer AV label format
        return [PRE, SUF, SUF]

    # TOK.TOK-TOK!TOK
    def parse_delim_fmt20(self, tokens):
        tax = [CAT, UNK, UNK, SUF]
        if tokens[0] in ["Exploit", "VirTool", "Constructor"]:
            tax = [CAT, VULN, VULN, SUF]
        elif tokens[2] == "based":
            tax = [CAT, FAM, SUF, SUF]
        else:
            tax = [CAT, FAM, FAM, SUF]
        return tax

    # TOK.TOK-TOK-TOK
    def parse_delim_fmt21(self, tokens):
        return [CAT, VULN, VULN, VULN]

    # TOK-TOK
    def parse_delim_fmt22(self, tokens):
        tax = [UNK, UNK]
        if tokens[0] == "Dropper":
            tax = [CAT, SUF]
        elif tokens[1].isnumeric() or len(tokens[1]) == 1:
            tax = [FAM, SUF]
        elif tokens[1] in ["family", "gen"]:
            tax = [FAM, SUF]
        else:
            tax = [FAM, FAM]
        return tax

    # TOK.TOK!TOK++TOK+TOK
    def parse_delim_fmt23(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK-TOK.TOK
    def parse_delim_fmt24(self, tokens):
        tax = [UNK, UNK, UNK]
        if tokens[1] == "Worm":
            tax = [CAT, CAT, FAM]
        else:
            if tokens[1] == "based":
                tax = [FAM, SUF, SUF]
            else:
                tax = [FAM, FAM, SUF]
        return tax

    # TOK_TOK.TOK.TOK
    def parse_delim_fmt25(self, tokens):
        return [FAM, FAM, SUF, SUF]

    # TOK/TOK.TOK
    def parse_delim_fmt26(self, tokens):
        return [PRE, PACK, SUF]

    # TOK.TOK.TOK!+TOK+TOK
    def parse_delim_fmt27(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK++TOK
    def parse_delim_fmt28(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK!
    def parse_delim_fmt29(self, tokens):
        return [CAT, FAM, NULL]

    # TOK.TOK!TOK+TOK
    def parse_delim_fmt30(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt31(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK/TOK
    def parse_delim_fmt32(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK+TOK
    def parse_delim_fmt33(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_delim_fmt34(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK!TOK
    def parse_delim_fmt35(self, tokens):
        return [PRE, SUF]

    # TOK.TOK!+TOK
    def parse_delim_fmt36(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK!
    def parse_delim_fmt37(self, tokens):
        return [CAT, CAT, FAM, NULL]

    # TOK.TOK
    def parse_delim_fmt38(self, tokens):
        tax = [UNK, UNK]
        if tokens[1].isnumeric() or len(tokens[1]) == 1:
            tax = [FAM, SUF]
        elif tokens[1] in ["Gen", "generic"]:
            tax = [FAM, SUF]
        else:
            tax = [PRE, FAM]
        return tax

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt39(self, tokens):
        tax = [UNK, UNK, UNK, UNK]
        if tokens[1] == "Worm":
            tax = [CAT, CAT, FAM, SUF]
        else:
            tax = [FAM, FAM, SUF, SUF]
        return tax

    # TOK.TOK!/TOK
    def parse_delim_fmt40(self, tokens):
        return [CAT, FAM, SUF]

    # TOK-TOK_TOK
    def parse_delim_fmt41(self, tokens):
        return [FAM, FAM, SUF]

    # TOK-TOK.TOK!TOK
    def parse_delim_fmt42(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK.TOK.TOK!TOK.TOK
    def parse_delim_fmt43(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK/TOK!TOK
    def parse_delim_fmt44(self, tokens):
        return [PRE, PACK, SUF]

    # TOK-TOK.TOK!TOK+TOK
    def parse_delim_fmt45(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK+TOK+TOK
    def parse_delim_fmt46(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!TOK/TOK/TOK
    def parse_delim_fmt47(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK!+TOK
    def parse_delim_fmt48(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK!TOK/TOK+TOK
    def parse_delim_fmt49(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!TOK+TOK/TOK
    def parse_delim_fmt50(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK
    def parse_delim_fmt51(self, tokens):
        return [FAM]

    # TOK.TOK.TOK!/TOK
    def parse_delim_fmt52(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK.TOK!TOK/TOK/TOK
    def parse_delim_fmt53(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK+TOK/TOK
    def parse_delim_fmt54(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

