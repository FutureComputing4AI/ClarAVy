from claravy.avparse import AVParse
from claravy.taxonomy import *


class AVStats_Map:

    def __init__(self, supported_avs):
        """Class for computing stats over a chunk of scan reports. Multiple
        AVStats_Map objects can run in parallel, and their results are
        aggregated by an AVStats object by calling reduce_stats().

        Arguments:
        supported_avs -- List of supported AV products.
        """

        self.valid_alias_fmts = set([FAM, CAT, TGT, PRE, UNK])
        self.valid_fam_fmts = set([FAM, UNK])
        self.valid_cat_fmts = set([CAT, PRE, UNK])
        self.valid_tgt_fmts = set([TGT, PRE, UNK])
        self.md5s = []
        self.av_counts = {av: 0 for av in supported_avs}
        self.label_md5s = {}
        self.token_md5s = {}
        self.related_tokens = {}
        self.token_fmt_counts = {}

    def update_stats(self, stats):
        md5_int = int(stats[0], 16)
        self.md5s.append(md5_int)

        fam_toks = set()
        cat_toks = set()
        tgt_toks = set()
        for av, label, tok_fmts in stats[1]:
            if self.label_md5s.get(label) is None:
                self.label_md5s[label] = set()
            self.label_md5s[label].add(md5_int)

            # Update stats for tokens
            for tok, fmt in tok_fmts:
                self.av_counts[av] += 1
                if self.token_md5s.get(tok) is None:
                    self.token_md5s[tok] = set()
                    self.related_tokens[tok] = set()
                if fmt in self.valid_alias_fmts: # TODO: Need to be careful about this
                    self.token_md5s[tok].add(md5_int)

                if self.token_fmt_counts.get(tok) is None:
                    self.token_fmt_counts[tok] = {fmt: 0}
                if self.token_fmt_counts[tok].get(fmt) is None:
                    self.token_fmt_counts[tok][fmt] = 0
                self.token_fmt_counts[tok][fmt] += 1

                if fmt in self.valid_fam_fmts:
                    fam_toks.add((av, tok, fmt))
                if fmt in self.valid_cat_fmts:
                    cat_toks.add((av, tok, fmt))
                if fmt in self.valid_tgt_fmts:
                    tgt_toks.add((av, tok, fmt))

        # Update related FAM tokens for current report
        for av1, tok1, fmt1 in fam_toks:
            if fmt1 != FAM:
                continue
            for av2, tok2, _ in fam_toks:
                if av1 == av2:
                    continue
                self.related_tokens[tok1].add(tok2)

        # Update related CAT tokens for current report
        for av1, tok1, fmt1 in cat_toks:
            if fmt1 != CAT:
                continue
            for av2, tok2, _ in cat_toks:
                if av1 == av2:
                    continue
                self.related_tokens[tok1].add(tok2)

        # Update related TGT tokens for current report
        for av1, tok1, fmt1 in tgt_toks:
            if fmt1 != TGT:
                continue
            for av2, tok2, _ in tgt_toks:
                if av1 == av2:
                    continue
                self.related_tokens[tok1].add(tok2)

        return


class AVStats:

    def __init__(self, supported_avs):
        """Class for computing and storing stats about AV scan reports.

        Arguments:
        supported_avs -- List of supported AV products.
        """

        # Updated by calling reduce_stats
        self.num_scans = 0
        self.md5_idxs = {}
        self.av_counts = {av: 0 for av in supported_avs}
        self.token_fmt_counts = {}
        self.token_md5s = {}
        self.related_tokens = {}

        # Updated by calling update_token_stats
        self.fmt_tokens = None
        self.token_counts = None


    def reduce_stats(self, av_stats_mapper):
        """Update stats using an AVStats mapper.

        Arguments:
        av_stats_mapper - an AVStats_Map object
        """

        # Reduce MD5s
        for md5 in av_stats_mapper.md5s:
            if self.md5_idxs.get(md5) is None:
                self.md5_idxs[md5] = self.num_scans
                self.num_scans += 1

        # Reduce AV counts
        for av, count in av_stats_mapper.av_counts.items():
            self.av_counts[av] += count

        # Reduce token FMT counts
        for tok, fmt_counts in av_stats_mapper.token_fmt_counts.items():
            if self.token_fmt_counts.get(tok) is None:
                self.token_fmt_counts[tok] = fmt_counts
            else:
                for fmt, count in fmt_counts.items():
                    if self.token_fmt_counts[tok].get(fmt) is None:
                        self.token_fmt_counts[tok][fmt] = count
                    else:
                        self.token_fmt_counts[tok][fmt] += count

        # Reduce token MD5s
        for tok, md5s in av_stats_mapper.token_md5s.items():
            md5_idxs = set([self.md5_idxs[md5] for md5 in md5s])
            if self.token_md5s.get(tok) is None:
                self.token_md5s[tok] = md5_idxs
            else:
                self.token_md5s[tok].update(md5_idxs)

        # Reduce related tokens
        for tok, related_toks in av_stats_mapper.related_tokens.items():
            if self.related_tokens.get(tok) is None:
                self.related_tokens[tok] = related_toks
            else:
                self.related_tokens[tok].update(related_toks)

        return


    def update_token_stats(self, token_vocab):
        """Calculates stats about each token's appearance in the dataset.
        Initializes stats about tokens in the user-defined taxonomy if they
        are not encountered in the dataset.

        Arguments:
        token_vocab -- Dict storing known vocabs for tokens
        """

        # Map vocab back to tokens, and track stats about tokens
        self.fmt_tokens = {}
        self.token_counts = {}
        for tok, fmt in token_vocab.items():

            # Map vocab -> tokens
            if self.fmt_tokens.get(fmt) is None:
                self.fmt_tokens[fmt] = set()
            self.fmt_tokens[fmt].add(tok)

            # Track token counts
            if self.token_fmt_counts.get(tok) is None:
                self.token_counts[tok] = 0
            else:
                self.token_counts[tok] = sum(self.token_fmt_counts[tok].values())

            # Track related tokens
            if self.related_tokens.get(tok) is None:
                self.related_tokens[tok] = set()

            # Map tokens to MD5s of scan reports
            if self.token_md5s.get(tok) is None:
                self.token_md5s[tok] = set()

        return
