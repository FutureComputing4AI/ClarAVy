from claravy.taxonomy import *


class Parse_Virit:

    def __init__(self):
        self.parse_delim_fmt = {
            "TOK.TOK.TOK.TOK": self.parse_delim_fmt1,
            "TOK.TOK.TOK": self.parse_delim_fmt2,
            "TOK.TOK.TOK_TOK.TOK": self.parse_delim_fmt3,
            "TOK.TOK.TOK-TOK.TOK": self.parse_delim_fmt4,
        }

    # TOK.TOK.TOK.TOK
    def parse_delim_fmt1(self, tokens):
        return [PRE, PRE, FAM, SUF]

    # TOK.TOK.TOK
    def parse_delim_fmt2(self, tokens):
        return [PRE, FAM, SUF]

    # TOK.TOK.TOK_TOK.TOK
    def parse_delim_fmt3(self, tokens):
        return [CAT, FILE, UNK, UNK, SUF]

    # TOK.TOK.TOK-TOK.TOK
    def parse_delim_fmt4(self, tokens):
        tax = [PRE, PRE, UNK, UNK, SUF]
        if len(tokens[2]) == 1:
            tax = [PRE, PRE, SUF, FAM, SUF]
        return tax    
    
    

    
