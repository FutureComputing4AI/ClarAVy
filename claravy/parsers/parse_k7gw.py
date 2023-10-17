from claravy.taxonomy import *


class Parse_K7gw: # K7antivirus and K7GW both owned by K7 Computing

    def __init__(self):
        self.parse_fmt = {
            "TOK ( TOK )": self.parse_fmt1,
            "TOK": self.parse_fmt2,
            "TOK-TOK ( TOK )": self.parse_fmt3,
            "TOK-TOK": self.parse_fmt4,
        }

    # TOK ( TOK )
    def parse_fmt1(self, tokens):
        return [CAT, SUF, NULL]

    # TOK
    def parse_fmt2(self, tokens):
        return [CAT]

    # TOK-TOK ( TOK )
    def parse_fmt3(self, tokens):
        return [CAT, CAT, SUF, NULL]

    # TOK-TOK
    def parse_fmt4(self, tokens):
        return [CAT, CAT]
