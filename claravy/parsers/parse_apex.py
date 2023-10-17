from claravy.taxonomy import *


class Parse_Apex:

    def __init__(self):
        self.parse_fmt = {
            "TOK": self.parse_fmt1,
            "TOK TOK TOK (TOK TOK TOK).": self.parse_fmt2,
        }

    # TOK
    def parse_fmt1(self, tokens):
        return [PRE] # Always 'Malicious'

    # TOK TOK TOK (TOK TOK TOK).
    def parse_fmt2(self, tokens):
        return [PRE, PRE, PRE, PRE, PRE, PRE, NULL]
