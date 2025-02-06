from claravy.taxonomy import *


class Parse_K7antivirus: # K7antivirus and K7GW both owned by K7 Computing

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK ( TOK )": self.parse_delim_fmt1,
            "TOK": self.parse_delim_fmt2,
            "TOK-TOK ( TOK )": self.parse_delim_fmt3,
            "TOK-TOK": self.parse_delim_fmt4,
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt5,
            "TOK.TOK.TOK": self.parse_delim_fmt6,
            "TOK-TOK.TOK.TOK.TOK": self.parse_delim_fmt7,
            "TOK-TOK.TOK.TOK": self.parse_delim_fmt8,
        }

    # TOK ( TOK )
    def parse_delim_fmt1(self, tokens):
        return [CAT, SUF, NULL]

    # TOK
    def parse_delim_fmt2(self, tokens):
        return [CAT]

    # TOK-TOK ( TOK )
    def parse_delim_fmt3(self, tokens):
        return [CAT, CAT, SUF, NULL]

    # TOK-TOK
    def parse_delim_fmt4(self, tokens):
        return [CAT, CAT]

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt5(self, tokens):
        return [CAT, FILE, FAM, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt6(self, tokens):
        return [CAT, FILE, FAM]

    # TOK-TOK.TOK.TOK.TOK
    def parse_delim_fmt7(self, tokens):
        return [CAT, CAT, FILE, FAM, SUF]

    # TOK-TOK.TOK.TOK
    def parse_delim_fmt8(self, tokens):
        tax = [CAT, CAT, FILE, UNK]
        if tokens[3].isupper():
            tax = [CAT, CAT, FILE, UNK]
        else:
            tax = [CAT, CAT, FILE, FAM]
        return tax
