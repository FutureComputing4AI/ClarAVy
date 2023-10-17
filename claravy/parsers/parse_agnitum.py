from claravy.taxonomy import *


class Parse_Agnitum: # Acquired Virusbuster, Acquired by Yandex

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
            "TOK.TOK!TOK": self.parse_fmt2,
            "TOK/TOK": self.parse_fmt3,
            "TOK.TOK.TOK": self.parse_fmt4,
            "TOK.TOK.TOK!TOK": self.parse_fmt5,
            "TOK.TOK!TOK/TOK": self.parse_fmt6,
            "TOK.TOK!TOK++TOK": self.parse_fmt7,
            "TOK.TOK.TOK!TOK/TOK+TOK": self.parse_fmt8,
            "TOK.TOK!/TOK/TOK": self.parse_fmt9,
            "TOK.TOK.TOK!TOK+TOK+TOK": self.parse_fmt10,
            "TOK.TOK!TOK/+TOK": self.parse_fmt11,
            "TOK.TOK.TOK.TOK!TOK": self.parse_fmt12,
            "TOK.TOK!+TOK/TOK": self.parse_fmt13,
            "TOK.TOK!+TOK+TOK": self.parse_fmt14,
            "TOK.TOK!TOK//TOK": self.parse_fmt15,
            "TOK.TOK!TOK+/TOK": self.parse_fmt16,
            "TOK.TOK!/TOK+TOK": self.parse_fmt17,
            "TOK_TOK.TOK": self.parse_fmt18,
            "TOK/TOK-TOK": self.parse_fmt19,
            "TOK.TOK-TOK!TOK": self.parse_fmt20,
            "TOK.TOK-TOK-TOK": self.parse_fmt21,
            "TOK-TOK": self.parse_fmt22,
            "TOK.TOK!TOK++TOK+TOK": self.parse_fmt23,
            "TOK-TOK.TOK": self.parse_fmt24,
            "TOK_TOK.TOK.TOK": self.parse_fmt25,
            "TOK/TOK.TOK": self.parse_fmt26,
            "TOK.TOK.TOK!+TOK+TOK": self.parse_fmt27,
            "TOK.TOK.TOK!TOK++TOK": self.parse_fmt28,
            "TOK.TOK!": self.parse_fmt29,
            "TOK.TOK!TOK+TOK": self.parse_fmt30,
            "TOK.TOK.TOK!TOK.TOK": self.parse_fmt31,
            "TOK.TOK.TOK!TOK/TOK": self.parse_fmt32,
            "TOK.TOK.TOK!TOK+TOK": self.parse_fmt33,
            "TOK.TOK.TOK.TOK.TOK": self.parse_fmt34,
            "TOK!TOK": self.parse_fmt35,
            "TOK.TOK!+TOK": self.parse_fmt36,
            "TOK.TOK.TOK!": self.parse_fmt37,
            "TOK.TOK": self.parse_fmt38,
            "TOK-TOK.TOK.TOK": self.parse_fmt39,
            "TOK.TOK!/TOK": self.parse_fmt40,
            "TOK-TOK_TOK": self.parse_fmt41,
            "TOK-TOK.TOK!TOK": self.parse_fmt42,
            "TOK.TOK.TOK.TOK!TOK.TOK": self.parse_fmt43,
            "TOK/TOK!TOK": self.parse_fmt44,
            "TOK-TOK.TOK!TOK+TOK": self.parse_fmt45,
            "TOK.TOK!TOK+TOK+TOK": self.parse_fmt46,
            "TOK.TOK!TOK/TOK/TOK": self.parse_fmt47,
            "TOK.TOK.TOK!+TOK": self.parse_fmt48,
            "TOK.TOK!TOK/TOK+TOK": self.parse_fmt49,
            "TOK.TOK!TOK+TOK/TOK": self.parse_fmt50,
            "TOK": self.parse_fmt51,
            "TOK.TOK.TOK!/TOK": self.parse_fmt52,
            "TOK.TOK.TOK!TOK/TOK/TOK": self.parse_fmt53,
            "TOK.TOK.TOK!TOK+TOK/TOK": self.parse_fmt54
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        fmt = [PRE, UNK, UNK, SUF]
        if tokens[2] == "Gen" or (tokens[2].isupper() and len(tokens[2]) <= 2):
            fmt[1] = FAM
            fmt[2] = SUF
        else:
            fmt[1] = PRE
            fmt[2] = FAM
        return fmt

    # TOK.TOK!TOK
    def parse_fmt2(self, tokens):
        return [CAT, FAM, SUF]

    # TOK/TOK
    def parse_fmt3(self, tokens):
        return [PRE, PACK]

    # TOK.TOK.TOK
    def parse_fmt4(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK!TOK
    def parse_fmt5(self, tokens):
        fmt = [CAT, CAT, FAM, SUF]
        if tokens[2] == "Gen":
            fmt = [CAT, FAM, SUF, SUF]
        return fmt

    # TOK.TOK!TOK/TOK
    def parse_fmt6(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK++TOK
    def parse_fmt7(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK/TOK+TOK
    def parse_fmt8(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!/TOK/TOK
    def parse_fmt9(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK+TOK+TOK
    def parse_fmt10(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!TOK/+TOK
    def parse_fmt11(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK!TOK
    def parse_fmt12(self, tokens):
        fmt = [CAT, UNK, UNK, UNK, SUF]
        if tokens[1].isupper() and len(tokens[1]) <= 3:
            if tokens[2].isupper() and len(tokens[2]) <= 3:
                fmt = [CAT, CAT, PRE, FAM, SUF]
            else:
                fmt = [CAT, CAT, FAM, SUF, SUF]
        else:
            fmt = [CAT, FAM, SUF, SUF, SUF]
        return fmt

    # TOK.TOK!+TOK/TOK
    def parse_fmt13(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!+TOK+TOK
    def parse_fmt14(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK//TOK
    def parse_fmt15(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK+/TOK
    def parse_fmt16(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK!/TOK+TOK
    def parse_fmt17(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK_TOK.TOK
    def parse_fmt18(self, tokens):
        return [FAM, FAM, SUF]

    # TOK/TOK-TOK
    def parse_fmt19(self, tokens): # Unusual packer AV label format
        return [PRE, SUF, SUF]

    # TOK.TOK-TOK!TOK
    def parse_fmt20(self, tokens):
        fmt = [CAT, UNK, UNK, SUF]
        if tokens[0] in ["Exploit", "VirTool", "Constructor"]:
            fmt = [CAT, VULN, VULN, SUF]
        elif tokens[2] == "based":
            fmt = [CAT, FAM, SUF, SUF]
        else:
            fmt = [CAT, FAM, FAM, SUF]
        return fmt

    # TOK.TOK-TOK-TOK
    def parse_fmt21(self, tokens):
        return [CAT, VULN, VULN, VULN]

    # TOK-TOK
    def parse_fmt22(self, tokens):
        fmt = [UNK, UNK]
        if tokens[0] == "Dropper":
            fmt = [CAT, SUF]
        elif tokens[1].isnumeric() or len(tokens[1]) == 1:
            fmt = [FAM, SUF]
        elif tokens[1] in ["family", "gen"]:
            fmt = [FAM, SUF]
        else:
            fmt = [FAM, FAM]
        return fmt

    # TOK.TOK!TOK++TOK+TOK
    def parse_fmt23(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK-TOK.TOK
    def parse_fmt24(self, tokens):
        fmt = [UNK, UNK, UNK]
        if tokens[1] == "Worm":
            fmt = [CAT, CAT, FAM]
        else:
            if tokens[1] == "based":
                fmt = [FAM, SUF, SUF]
            else:
                fmt = [FAM, FAM, SUF]
        return fmt

    # TOK_TOK.TOK.TOK
    def parse_fmt25(self, tokens):
        return [FAM, FAM, SUF, SUF]

    # TOK/TOK.TOK
    def parse_fmt26(self, tokens):
        return [PRE, PACK, SUF]

    # TOK.TOK.TOK!+TOK+TOK
    def parse_fmt27(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK++TOK
    def parse_fmt28(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK!
    def parse_fmt29(self, tokens):
        return [CAT, FAM, NULL]

    # TOK.TOK!TOK+TOK
    def parse_fmt30(self, tokens):
        return [CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK.TOK
    def parse_fmt31(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK/TOK
    def parse_fmt32(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK!TOK+TOK
    def parse_fmt33(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK.TOK.TOK.TOK
    def parse_fmt34(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK!TOK
    def parse_fmt35(self, tokens):
        return [PRE, SUF]

    # TOK.TOK!+TOK
    def parse_fmt36(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK!
    def parse_fmt37(self, tokens):
        return [CAT, CAT, FAM, NULL]

    # TOK.TOK
    def parse_fmt38(self, tokens):
        fmt = [UNK, UNK]
        if tokens[1].isnumeric() or len(tokens[1]) == 1:
            fmt = [FAM, SUF]
        elif tokens[1] in ["Gen", "generic"]:
            fmt = [FAM, SUF]
        else:
            fmt = [PRE, FAM]
        return fmt

    # TOK-TOK.TOK.TOK
    def parse_fmt39(self, tokens):
        fmt = [UNK, UNK, UNK, UNK]
        if tokens[1] == "Worm":
            fmt = [CAT, CAT, FAM, SUF]
        else:
            fmt = [FAM, FAM, SUF, SUF]
        return fmt

    # TOK.TOK!/TOK
    def parse_fmt40(self, tokens):
        return [CAT, FAM, SUF]

    # TOK-TOK_TOK
    def parse_fmt41(self, tokens):
        return [FAM, FAM, SUF]

    # TOK-TOK.TOK!TOK
    def parse_fmt42(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK.TOK.TOK!TOK.TOK
    def parse_fmt43(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK/TOK!TOK
    def parse_fmt44(self, tokens):
        return [PRE, PACK, SUF]

    # TOK-TOK.TOK!TOK+TOK
    def parse_fmt45(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF]

    # TOK.TOK!TOK+TOK+TOK
    def parse_fmt46(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!TOK/TOK/TOK
    def parse_fmt47(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK!+TOK
    def parse_fmt48(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK!TOK/TOK+TOK
    def parse_fmt49(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK!TOK+TOK/TOK
    def parse_fmt50(self, tokens):
        return [CAT, FAM, SUF, SUF, SUF]

    # TOK
    def parse_fmt51(self, tokens):
        return [FAM]

    # TOK.TOK.TOK!/TOK
    def parse_fmt52(self, tokens):
        return [CAT, CAT, FAM, SUF]

    # TOK.TOK.TOK!TOK/TOK/TOK
    def parse_fmt53(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

    # TOK.TOK.TOK!TOK+TOK/TOK
    def parse_fmt54(self, tokens):
        return [CAT, CAT, FAM, SUF, SUF, SUF]

