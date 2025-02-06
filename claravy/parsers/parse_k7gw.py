from claravy.taxonomy import *


class Parse_K7gw: # K7antivirus and K7GW both owned by K7 Computing

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK ( TOK )": self.parse_delim_fmt1,
            "TOK": self.parse_delim_fmt2,
            "TOK-TOK ( TOK )": self.parse_delim_fmt3,
            "TOK-TOK": self.parse_delim_fmt4,
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
