import re
import pylcs
import logging
import editdistance
from claravy.avparse import AVParse
from claravy.avstats import AVStats
from claravy.taxonomy import *

logger = logging.getLogger("ClarAVy")


class AVAlias:

    def __init__(self, av_stats, token_vocab, alias_mapping, substring_path):
        """Class for identifying token aliases in AV scan data.

        Arguments:
        av_stats -- An AVStats object
        token_vocab -- Dict storing known vocabs for tokens
        av_stats -- AVStats object for tracking stats about AV scan data.
        substring_path -- Path to file containing prefix/suffix substrings.
        """

        # Initialize token, parent, child aliases        
        self.av_stats = av_stats
        self.alias_mapping = alias_mapping
        self.token_substrings = self.read_substrings(substring_path)
        self.VOWEL_REPLACE = re.compile(r"[aeiou]")
        self.valid_fmts = set([FAM, CAT, TGT, PACK, PRE, UNK])
        self.token_aliases = {}
        self.parent_aliases = {}
        self.child_aliases = {}
        for fmt, toks in av_stats.fmt_tokens.items():
            if fmt not in self.valid_fmts:
                continue
            for tok in toks:
                self.token_aliases[tok] = set([tok])
                self.parent_aliases[tok] = set()
                self.child_aliases[tok] = set()

        # Separate alias mapping by vocab
        self.fmt_alias_mapping = {fmt: {} for fmt in self.valid_fmts}

        # Get canonical tokens
        self.known_canonical_tokens = {fmt: set() for fmt in self.valid_fmts}
        for alias, canonical_tok in self.alias_mapping.items():
            fmt = token_vocab[canonical_tok]
            self.fmt_alias_mapping[fmt][alias] = canonical_tok
            self.known_canonical_tokens[fmt].add(canonical_tok)
        all_canonical_tokens = set()
        for fmt in self.valid_fmts:
            all_canonical_tokens.update(self.known_canonical_tokens[fmt])

        # Read token substrings
        self.token_substrings = self.read_substrings(substring_path)

        # Identify child alias candidates for CAT and TGT tokens
        for fmt in [CAT, TGT]:
            self.resolve_child_aliases(fmt)

        # Resolve any aliases given in the alias wordlist
        for fmt in [CAT, TGT, PACK]:
            for tok1, tok2 in self.fmt_alias_mapping[fmt].items():
                self.resolve_alias_pair(tok1, tok2)

        # Resolve trivial aliases
        for fmt in [CAT, TGT, PACK]:
            self.resolve_trivial_aliases(fmt)

        # Update alias mapping
        for fmt in [CAT, TGT, PACK]:
            fmt_alias_mapping = self.get_fmt_alias_mapping(fmt)
            sorted_canonical_tokens = sorted(fmt_alias_mapping.keys())
            for canonical_tok in sorted_canonical_tokens:
                if self.fmt_alias_mapping[fmt].get(canonical_tok) is not None:
                    continue
                for alias in fmt_alias_mapping[canonical_tok]:
                    if (alias in all_canonical_tokens or
                        self.fmt_alias_mapping[fmt].get(alias) is not None):
                        continue
                    self.fmt_alias_mapping[fmt][alias] = canonical_tok
                    if self.alias_mapping.get(alias) is None:
                        self.alias_mapping[alias] = canonical_tok


    def read_substrings(self, substring_path):
        """Read token subsrings. These are used for identifying tokens starting
        or ending in certain substrings.

        Arguments:
        substring_path -- Path to file with token substrings.
        """

        token_substrings = {}
        with open(substring_path, "r") as f:
            cur_type = None
            for line in f:
                line = line.strip()
                if not len(line):
                    continue
                if line.startswith("["):
                    cur_type = line[1:-1]
                    token_substrings["{}_{}".format("PRE", cur_type)] = set()
                    token_substrings["{}_{}".format("SUF", cur_type)] = set()
                elif line.startswith("-"):
                    key = "{}_{}".format("PRE", cur_type)
                    token_substrings[key].add(line[1:])
                elif line.endswith("-"):
                    key = "{}_{}".format("SUF", cur_type)
                    token_substrings[key].add(line[:-1])

        return token_substrings


    def resolve_alias_pair(self, tok1, tok2):
        """Resolve a pair of token aliases, updating their statistics.

        Arguments: 
        tok1 -- A token
        tok2 -- Another token that is an alias of tok1
        """

        # Combine info from all aliases
        all_scan_idxs = set()
        all_related_tokens = set()
        all_aliases = set()
        for tok in [tok1, tok2]:
            scan_idxs = self.av_stats.token_md5s[tok]
            all_scan_idxs.update(scan_idxs)
            all_related_tokens.update(self.av_stats.related_tokens[tok])
            all_aliases.update(self.token_aliases[tok])

        # Determine canonical token
        canonical_tok = sorted(all_aliases,
                               key=lambda tok: self.av_stats.token_counts[tok],
                               reverse=True)[0]

        # Make sure canonical token does not end in a digit
        if canonical_tok[-1].isnumeric() and canonical_tok[:-1] in all_aliases:
            canonical_tok = canonical_tok[:-1]

        # Defer to a hard-coded canonical token, if there is one
        # Return without resolving aliases if this would cause a conflict
        canonical_toks = [tok for tok in all_aliases
                          if tok in self.known_canonical_tokens]
        if len(canonical_toks) >= 2:
            return
        elif len(canonical_toks) == 1:
            canonical_tok = canonical_toks[0]

        # Update canonical token info
        self.av_stats.token_md5s[canonical_tok] = all_scan_idxs
        self.av_stats.related_tokens[canonical_tok] = all_related_tokens
        self.token_aliases[canonical_tok] = all_aliases

        # Make all other aliases reference canonical token
        for tok in self.token_aliases[tok1] | self.token_aliases[tok2]:
            if tok == canonical_tok:
                continue
            self.av_stats.token_md5s[tok] = self.av_stats.token_md5s[canonical_tok]
            self.av_stats.related_tokens[tok] = self.av_stats.related_tokens[canonical_tok]
            self.token_aliases[tok] = self.token_aliases[canonical_tok]

        return


    def edit_pct(self, tok1, tok2):
        """Compute edit distance percentage between tokens.

        Many aliases have very similar spellings. Examples include adding
        digits/characters, using slight spelling changes, reversing the name of
        the token, or abbreviating parts of the token.
        """

        # Compute edit distance between tok1 and tok2
        # Divide by length of longest token name to get edit perecent
        # Edit percent has range [0.0, 1.0]
        # 0.0 -> tok1 and tok2 are identical, 1.0 -> tok1 and tok2 are distant
        tok_short, tok_long = sorted([tok1, tok2], key=lambda l:len(l))
        min_len, max_len = len(tok_short), len(tok_long)
        edit_pct = editdistance.eval(tok1, tok2) / max_len

        # Many aliases are the names of tokens backwards, or are anagrams.
        # Override edit pct for anagrams.
        if min_len >= 6 and edit_pct > 0.25 and sorted(tok1) == sorted(tok2):
            edit_pct = 0.25

        # Override edit pct for tokens that are subsets of other tokens
        lcs_len = pylcs.lcs_sequence_length(tok_long, tok_short)
        if min_len >= 4 and lcs_len == min_len and edit_pct > 0.25:
            edit_pct = 0.25

        return edit_pct


    def co_occur_pct(self, tok1, tok2):
        """Returns the co-occurrence percentage for two tokens."""

        # Get scan reports that both tokens occur in
        tok1_scans = self.av_stats.token_md5s[tok1]
        tok2_scans = self.av_stats.token_md5s[tok2]
        intersect = len(tok1_scans.intersection(tok2_scans))
        min_occur, _ = sorted([len(tok1_scans), len(tok2_scans)])
        co_occur_pct = intersect / min_occur
        return co_occur_pct


    def get_total_count(self, tok):
        """Returns the total number of scan reports that the token and any of
        its known aliases appears in."""
        return len(self.av_stats.token_md5s[tok])


    def get_sorted_aliases(self, fmt):
        """Returns a list of tuples, where each tuple contains a known cluster
        of trivial/sibling aliases. Each cluster is sorted by largest ->
        smallest token, and the clusters are sorted from largest -> smallest
        alias cluster.

        Arguments:
        fmt -- The token vocab
        """

        # Get all known tokens for fmt
        known_tokens = set(self.av_stats.fmt_tokens[fmt].values())

        # Get set of all known trivial/sibling alias clusters
        aliases = set()
        for tok in known_tokens:
            tok_aliases = list(sorted(self.token_aliases[tok]))
            tok_aliases.sort(key=lambda tok: self.av_stats.token_counts[tok],
                             reverse=True)
            aliases.add(tuple(tok_aliases))

        # Sort by size of alias cluster
        aliases = list(aliases)
        aliases.sort(key=lambda a: self.get_total_count(a[0]), reverse=True)
        return aliases


    def resolve_trivial_aliases(self, fmt):
        """Resolve trivial aliases - token ending with an extra digit.

        Arguments:
        fmt -- The token vocab
        """

        # Get list of all known tokens in vocab
        known_tokens = self.av_stats.fmt_tokens[fmt]
        expanded_tokens = known_tokens.copy()
        if fmt in [CAT, TGT]:
            expanded_tokens.update(self.av_stats.fmt_tokens[PRE])

        # Identify tokens that are variants of known tokens which have
        # predictable substring suffixes/prefixes
        to_resolve = []
        for tok in expanded_tokens:
            if len(tok) <= 6:
                continue

            # Identical except for an extra digit
            if tok[-1].isnumeric() and tok[:-1] in known_tokens:
                to_resolve.append((tok, tok[:-1]))
                continue

            # Identical except for an extra character
            if len(tok) >= 10 and tok[:-1] in known_tokens:
                to_resolve.append((tok, tok[:-1]))
                continue

            # Identical except for a prefix
            found_pre = False
            for pre in self.token_substrings["PRE_SUBSTR"]:
                if len(tok) > len(pre) and tok.endswith(pre):
                    if tok[len(pre):] in known_tokens:
                        to_resolve.append((tok, tok[len(pre):]))
                        found_pre = True
                        break
            if found_pre:
                continue

            # Identical except for a suffix
            for suf in self.token_substrings["SUF_SUBSTR"]:
                if len(tok) > len(suf) and tok.endswith(suf):
                    if tok[:len(suf)*-1] in known_tokens:
                        to_resolve.append((tok, tok[:len(suf)*-1]))
                        break

        # Resolve trivial aliases
        num_resolved = 0
        for tok1, tok2 in to_resolve:
            self.resolve_alias_pair(tok1, tok2)
            num_resolved += 1

        return


    def resolve_child_aliases(self, fmt, E=0.4, C=0.5):
        """Resolves 'parent/child' aliases.

        Due to differences in granualirity, one token have a one-way
        relationship with another token. By this, we mean that one token (which
        we call a child token) is smaller than a second (a parent token), and
        the parent token almost always co-occurs in scan reports containing
        the child token. However, since the parent token is more widespread,
        there are scan reports where it occurs but the child token does not.

        We identify parent/child aliases as pairs of tokens with high weak
        co-occurrence percentage and low token edit percent.

        Arguments:
        fmt -- The token vocab
        E -- Threshold for edit percent
        C -- Threshold for combined weak co-occurrence percentage and edit
             percentage, (1 - edit_pct) * weak_co_occur_pct
        """

        # Sort tokens by count (largest -> smallest)
        # Give priority to known canonical tokens
        known_canonical = self.known_canonical_tokens[fmt]
        unknown_tokens = [tok for tok in self.av_stats.fmt_tokens[fmt]
                          if tok not in known_canonical]
        known_canonical = list(known_canonical)
        known_canonical.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        unknown_tokens.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        sorted_tokens = known_canonical + unknown_tokens
        remaining_tokens = set(sorted_tokens)
        if fmt in [CAT, TGT]:
            remaining_tokens.update(self.av_stats.fmt_tokens[PRE])

        # Iterate over tokens
        for tok1 in sorted_tokens:
            remaining_tokens.remove(tok1)

            # Iterate over every token known to co-occur with tok1
            for tok2 in self.av_stats.related_tokens[tok1]:
                if tok2 not in remaining_tokens:
                    continue

                # Compute edit percentage between tok1 and tok2
                edit_pct = self.edit_pct(tok1, tok2)
                if edit_pct >= E:
                    continue

                # Use a combination of edit pct and co-occurrence percent for
                # identifying parent/child aliases
                co_occur_pct = self.co_occur_pct(tok1, tok2)
                if (1 - edit_pct) * co_occur_pct >= C:
                    self.child_aliases[tok1].add(tok2)
                    self.parent_aliases[tok2].add(tok1)

        return


    def get_fmt_alias_mapping(self, fmt, E=0.6):
        """Returns dict where the key is the canonical (most common) name of a
        token, and the value is a list of its aliases.

        Argument:
        fmt -- Current token vocabulary (e.g. CAT, TGT, etc.)
        E -- Threshold based on edit score and co-occurrence percentage
        """

        # Sort tokens by count (largest -> smallest)
        # Give priority to known canonical tokens
        known_canonical = self.known_canonical_tokens[fmt]
        unknown_tokens = [tok for tok in self.av_stats.fmt_tokens[fmt]
                          if tok not in known_canonical]
        known_canonical = list(known_canonical)
        known_canonical.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        unknown_tokens.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        sorted_tokens = known_canonical + unknown_tokens
        remaining_tokens = set(sorted_tokens)

        # Iterate over all tokens
        fmt_alias_mapping = {}
        for tok1 in sorted_tokens:
            if tok1 not in remaining_tokens:
                continue
            remaining_tokens.remove(tok1)

            # Form queue from current token's aliases and child aliases
            alias_queue = self.token_aliases[tok1]
            alias_queue = alias_queue.union(self.child_aliases[tok1])
            alias_queue = list(alias_queue)

            # Recursively get all children of the canonical token
            # For CAT and TGT tokens, stop recursing if the alias would have
            # too large of an edit distance from the canonical token
            aliases = set()
            while len(alias_queue):
                tok2 = alias_queue.pop(0)
                if tok2 not in remaining_tokens or tok2 in aliases:
                    continue

                # Don't expand tok2 if it (or its aliases) have a different
                # canonical token
                has_different_canonical = False
                for tok in self.token_aliases[tok2]:
                    if (self.fmt_alias_mapping[fmt].get(tok) is not None and
                    self.fmt_alias_mapping[fmt][tok] != tok1):
                        has_different_canonical = True
                if has_different_canonical:
                    continue

                # Expand queue with aliases of tok2
                alias_queue += list(self.token_aliases[tok2])
                alias_queue += list(self.child_aliases[tok2])
                aliases.add(tok2)

            # Add canonical token and aliases to mapping
            if not len(aliases):
                continue
            for tok2 in aliases:
                remaining_tokens.remove(tok2)
            aliases = [tok for tok in aliases
                       if self.fmt_alias_mapping[fmt].get(tok) is None]
            fmt_alias_mapping[tok1] = sorted(aliases)

        return fmt_alias_mapping


    def write_alias_mapping(self, alias_file):
        """Write the generated alias mapping to alias_file."""

        write_fmts = [CAT, TGT, PACK]
        with open(alias_file, "w") as f:
            for fmt in write_fmts:
                f.write("[{}]\n".format(fmt))
                sorted_fmt_aliases = list(self.fmt_alias_mapping[fmt].items())
                sorted_fmt_aliases.sort(key=lambda l:l[1])
                for alias, canonical_token in sorted_fmt_aliases:
                    f.write("{}\t{}\n".format(alias, canonical_token))
                f.write("\n")
        return
