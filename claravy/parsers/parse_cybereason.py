from claravy.taxonomy import *


class Parse_Cybereason:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK": self.parse_fmt1,
        }


    def parse_fmt1(self, tokens):
        return [PRE, SUF]
