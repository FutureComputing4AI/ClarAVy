from claravy.taxonomy import *


class Parse_Acronis:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK": self.parse_delim_fmt1
        }


    def parse_delim_fmt1(self, tokens):
        return [PRE]
