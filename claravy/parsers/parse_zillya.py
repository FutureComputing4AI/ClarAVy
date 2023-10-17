from claravy.taxonomy import *


class Parse_Zillya:

    def __init__(self):
        self.parse_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_fmt1,
        }

    # TOK.TOK.TOK.TOK
    def parse_fmt1(self, tokens):
        return [CAT, FAM, TGT, SUF] # Zillya format is incredibly standardized
