import sys
import pylcs
import random
import logging
import editdistance
from claravy.avparse import AVParse
from claravy.avstats import AVStats
from claravy.taxonomy import *

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("ClarAVy")


class AVAlias:

    def __init__(self, av_stats, token_vocab, av_parser, alias_mapping,
                 substring_path):
        """Class for identifying token aliases in AV scan data.

        Arguments:
        av_stats -- An AVStats object
        token_vocab -- Dict storing taxonomy assignments for tokens
        av_parser -- An AVParse object
        alias_mapping -- Path to file containing any user-defined aliases.
        substring_path -- Path to file containing prefix/suffix substrings.
        """

        self.av_stats = av_stats
        self.token_vocab = token_vocab
        self.av_parser = av_parser
        self.token_aliases = {}
        self.parent_aliases = {}
        self.child_aliases = {}

        # Initialize token, parent, child aliases
        valid_taxs = {FAM, GRP, CAT, FILE, PACK, PRE, UNK}
        for tax, toks in av_stats.tax_tokens.items():
            if tax not in valid_taxs:
                continue
            for tok in toks:
                self.token_aliases[tok] = {tok}
                self.parent_aliases[tok] = set()
                self.child_aliases[tok] = set()

        # Separate alias mapping by token taxonomy
        self.tax_alias_mapping = {tax: {} for tax in valid_taxs}

        # Get canonical token from each alias pair
        self.known_canonical_tokens = {tax: set() for tax in valid_taxs}
        for alias, canonical_tok in alias_mapping.items():
            tax = token_vocab[canonical_tok]
            self.tax_alias_mapping[tax][alias] = canonical_tok
            self.known_canonical_tokens[tax].add(canonical_tok)
        all_canonical_tokens = set()
        for tax in valid_taxs:
            all_canonical_tokens.update(self.known_canonical_tokens[tax])

        # Read token substrings from file
        self.token_substrings = self.read_substrings(substring_path)

        # Identify parent/child alias candidates for FAM, CAT, and FILE tokens
        for tax in [FAM, CAT, FILE]:
            self.resolve_child_aliases(tax)

        # Resolve any aliases given in the alias wordlist
        for tax in [FAM, CAT, FILE, PACK]:
            for tok1, tok2 in self.tax_alias_mapping[tax].items():
                self.resolve_alias_pair(tok1, tok2, tax)

        # Identify sibling FAM aliases
        self.resolve_sibling_aliases()

        # Resolve trivial aliases
        for tax in [FAM, CAT, FILE, PACK]:
            self.resolve_trivial_aliases(tax)

        # Build updated alias mapping
        self.alias_mapping = alias_mapping
        for tax in [FAM, CAT, FILE, PACK]:
            tax_alias_mapping = self.get_tax_alias_mapping(tax)
            sorted_canonical_tokens = sorted(tax_alias_mapping.keys())
            for canonical_tok in sorted_canonical_tokens:
                if self.tax_alias_mapping[tax].get(canonical_tok) is not None:
                    continue
                for alias in tax_alias_mapping[canonical_tok]:
                    if (alias in all_canonical_tokens or
                        self.tax_alias_mapping[tax].get(alias) is not None):
                        continue
                    self.tax_alias_mapping[tax][alias] = canonical_tok
                    if self.alias_mapping.get(alias) is None:
                        self.alias_mapping[alias] = canonical_tok


    def read_substrings(self, substring_path):
        """Read token subsrings. These are used for identifying aliases
        of tokens which start with predictable substrings. For example, the
        substring 'hp-' is an extremely common prefix used by some AV products.
        The token 'hpneutrino' would automatically be identified as an alias of
        the neutrino family.

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
                    key = "{}_{}".format("SUF", cur_type)
                    token_substrings[key].add(line[1:])
                elif line.endswith("-"):
                    key = "{}_{}".format("PRE", cur_type)
                    token_substrings[key].add(line[:-1])

        return token_substrings


    def resolve_alias_pair(self, tok1, tok2, tax):
        """Given a pair of aliases, update statistics in AVStats object so
        that the two tokens are equivalent.

        Arguments: 
        tok1 -- A token
        tok2 -- Another token that is an alias of tok1
        tax -- Taxonomy assignment of tok1
        """

        # Combine info from all aliases
        all_aliases = set()
        all_related_tokens = set()
        all_token_av_labels = {}
        for tok in [tok1, tok2]:
            all_aliases.update(self.token_aliases[tok])
            all_related_tokens.update(self.av_stats.related_tokens[tok])
            for av, labels in self.av_stats.token_av_labels[tok].items():
                if all_token_av_labels.get(av) is None:
                    all_token_av_labels[av] = set()
                all_token_av_labels[av].update(labels)

        # Defer to a hard-coded canonical token, if there is one
        # Return without resolving aliases if this would cause a conflict
        canonical_tok = None
        canonical_toks = [tok for tok in all_aliases
                          if tok in self.known_canonical_tokens[tax]]
        if len(canonical_toks) >= 2:
            return
        elif len(canonical_toks) == 1:
            canonical_tok = canonical_toks[0]

        # If there is not a hard-coded canonical token, pick one
        if canonical_tok is None:
            possible_canonical = []
            for tok in all_aliases:
                if self.token_vocab.get(tok) is None:
                    continue
                tok_tax = self.token_vocab[tok]
                if tok_tax != tax:
                    continue
                if self.av_stats.token_avs.get(tok) is None:
                    continue
                tok_count = self.av_stats.token_counts[tok]
                tok_avs = self.av_stats.token_avs[tok]
                tok_av_count = self.av_parser.get_av_count(tok, tok_avs)
                tok_score = tok_count * tok_av_count
                possible_canonical.append((tok, tok_score))
            canonical_tok = sorted(possible_canonical,
                                   key=lambda l:l[1], reverse=True)[0][0]

            # Make sure canonical token does not end in a digit
            if (canonical_tok[-1].isnumeric() and
                canonical_tok[:-1] in all_aliases):
                canonical_tok = canonical_tok[:-1]

        # Update canonical token info
        self.token_aliases[canonical_tok] = all_aliases
        self.av_stats.related_tokens[canonical_tok] = all_related_tokens
        self.av_stats.token_av_labels[canonical_tok] = all_token_av_labels

        # Make all other aliases reference canonical token
        for tok in self.token_aliases[tok1] | self.token_aliases[tok2]:
            self.token_vocab[tok] = tax
            if tok == canonical_tok:
                continue
            self.token_aliases[tok] = self.token_aliases[canonical_tok]
            related_toks = self.av_stats.related_tokens[canonical_tok]
            self.av_stats.related_tokens[tok] = related_toks
            self.av_stats.token_av_labels[tok] = all_token_av_labels

        return


    def edit_pct(self, tok1, tok2):
        """Compute edit distance percentage between tokens.

        Many token aliases have very similar spellings. Examples include adding
        digits/characters, using slight spelling changes, reversing the name of
        the token, or abbreviating parts of the token.
        """

        # Compute edit distance between tok1 and tok2
        # Divide by length of longest token name to get edit perecent
        # Edit percent has range [0.0, 1.0]. An edit percent of 0.0 means that
        # tok1 and tok2 are identical. An edit percent of 1.0 means that tok1
        # and tok2 have very dissimilar spelling.
        tok_short, tok_long = sorted([tok1, tok2], key=lambda l:len(l))
        min_len, max_len = len(tok_short), len(tok_long)

        # If either token is too short, override score to make them distant
        if min_len <= 5:
            return 1.0
        edit_pct = editdistance.eval(tok1, tok2) / max_len

        # Many aliases are the names of tokens backwards, or are anagrams.
        # Override edit pct for anagrams.
        if min_len >= 6 and sorted(tok1) == sorted(tok2):
            edit_pct = 0.01

        # Override edit pct for tokens that are subsets of other tokens
        lcs_len = pylcs.lcs_sequence_length(tok_long, tok_short)
        if edit_pct > 0.25 and lcs_len == min_len:
            edit_pct = 0.25
        elif edit_pct > 0.25 and (lcs_len / min_len) > 0.75:
            edit_pct = 0.25
        if tok_short in tok_long:
            if min_len >= 8:
                edit_pct = 0.01
            elif min_len >= 6 and (min_len / max_len) > 0.66:
                edit_pct = 0.01
            else:
                remaining = tok_long.replace(tok_short, "")
                if self.token_vocab.get(remaining) in [CAT, FILE]:
                    edit_pct = 0.01

        return edit_pct


    def co_occur_pct(self, tok1_scans, tok2_scans, pct_type="strong"):
        """Returns the co-occurrence percentage for two tokens.

        Arguments:
        tok1_scans -- Set of scan IDs where tok1 appears
        tok2_scans -- Set of scan IDs where tok2 appears
        pct_type -- Whether to compute strong or weak co-occurrence percent

        Many aliases are likely to occur with each other in the same scan
        report. We use 'weak' and 'strong' co-occurrence percentage to identify
        these aliases.

        Weak co-occurrence pct: # of scan reports which both tokens occur in,
        divided by # of scan reports which the smaller token occurs in.

        Strong co-occurrence pt: # of scan reports which both tokens occur in,
        divided by # of scan reports which the larger token occurs in.
        """

        if len(tok1_scans) == 0 or len(tok2_scans) == 0:
            return 0.0
        if pct_type != "strong":
            pct_type = "weak"

        # Swap tok1_scans and tok2_scans if tok1_scans is the larger set
        if len(tok1_scans) > len(tok2_scans):
            tok2_scans, tok1_scans = tok1_scans, tok2_scans
        min_occur, max_occur = len(tok1_scans), len(tok2_scans)

        # Handle strong co-occurrence pct
        if pct_type == "strong":
            intersect = len(tok1_scans.intersection(tok2_scans))
            strong_co_occur_pct = intersect / max_occur
            return strong_co_occur_pct

        # Handle weak co-occurrence pct
        # If we have very large sets of scan IDs, we'll save time by
        # approximating with 1,000 samples from the smaller set
        if min_occur > 1000:
            min_occur = 1000
            tok1_scans = set(random.sample(list(tok1_scans), min_occur))

        intersect = len(tok1_scans.intersection(tok2_scans))
        weak_co_occur_pct = intersect / min_occur
        return weak_co_occur_pct


    def get_total_count(self, tok):
        """Returns the total number of scan reports that the token and any of
        its known aliases appears in."""

        label_idxs = set()
        for av, labels in self.av_stats.token_av_labels[tok].items():
            for label in labels:
                label_idxs.update(self.av_stats.av_label_scans[av][label])
        return len(label_idxs)


    def get_sorted_aliases(self, tax):
        """Returns a list of tuples, where each tuple contains a known cluster
        of trivial/sibling aliases. Each cluster is sorted by most common ->
        least common token, and the clusters are sorted from largest ->
        smallest alias cluster.

        Arguments:
        tax -- The type of token to process (i.e. get all FAM aliases, sorted)
        """

        # Get all known tokens in current tax
        known_tokens = self.av_stats.tax_tokens[tax]

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


    def resolve_trivial_aliases(self, tax):
        """Resolve trivial aliases - tokens that are nearly identical, and
        obviously have the same meaning.

        Arguments:
        tax -- The type of token to process
        """

        # Get list of all known tokens in vocab
        known_tokens = self.av_stats.tax_tokens[tax]

        # Some PRE tokens may be CAT or FILE tokens
        # Some UNK tokens may be FAM tokens
        expanded_tokens = known_tokens.copy()
        if tax in [CAT, FILE]:
            expanded_tokens.update(self.av_stats.tax_tokens[PRE])
        if tax == FAM:
            expanded_tokens.update(self.av_stats.tax_tokens[UNK])

        # Identify tokens that are variants of known tokens which have
        # predictable substring suffixes/prefixes
        to_resolve = []
        for tok in expanded_tokens:

            # Identical except for an extra digit
            if (len(tok) >= 4 and tok[-1].isnumeric() and not
                tok[-2].isnumeric() and tok[:-1] in known_tokens):
                to_resolve.append((tok, tok[:-1]))
                continue

            # Identical except for an extra character
            if len(tok) >= 8 and tok[:-1] in known_tokens:
                to_resolve.append((tok, tok[:-1]))
                continue

            if len(tok) <= 3:
                continue

            # Identical except for a prefix
            found_pre = False
            for pre in self.token_substrings["PRE_SUBSTR"]:
                if len(tok) > len(pre) and tok.startswith(pre):
                    if tok[len(pre):] in known_tokens:
                        to_resolve.append((tok, tok[len(pre):]))
                        found_pre = True
                        break

            # Identical except for a suffix
            for suf in self.token_substrings["SUF_SUBSTR"]:
                if len(tok) > len(suf) and tok.endswith(suf):
                    if tok[:len(suf)*-1] in known_tokens:
                        to_resolve.append((tok, tok[:len(suf)*-1]))
                        break

        # Resolve trivial aliases
        num_resolved = 0
        for tok1, tok2 in to_resolve:
            self.resolve_alias_pair(tok1, tok2, tax)
            num_resolved += 1

        return


    def resolve_sibling_aliases(self, S=0.95, T=1000):
        """Resolves 'sibling' family aliases.

        Sibling aliases are tokens that nearly always co-occur with each other
        in both directions (e.g. if one token appears in a scan report, then
        the other nearly always does, and vice-versa).

        Arguments:
        S -- Strong co-occurrence threshold, default = 0.95
        T -- Minimum number of occurrences of the more common token
        """

        # Iterate until no new aliases are found
        total_resolved = 0
        num_resolved = 1
        while num_resolved > 0:

            # Iterate over alias clusters
            num_resolved = 0
            aliases = self.get_sorted_aliases(FAM)
            for alias_cluster in aliases:

                # Choose the canonial token for the alias cluster
                tok1 = alias_cluster[0]
                if len(tok1) <= 4:
                    continue
                tok1_tax = self.token_vocab[tok1]
                tok1_count = self.get_total_count(tok1)
                tok1_avs = self.av_stats.token_avs[tok1]
                tok1_av_count = self.av_parser.get_av_count(tok1, tok1_avs)
                if tok1_count < T:
                    continue

                # Initialize set of scans tok1 appears in
                # We will compute this later if needed
                tok1_scans = set()

                # Iterate over related tokens
                related_toks = self.av_stats.related_tokens[tok1]
                for tok2 in related_toks:
                    if len(tok2) <= 4:
                        continue
                    if tok2 in alias_cluster:
                        continue
                    if self.token_aliases.get(tok2) is not None:
                        if tok1 in self.token_aliases[tok2]:
                            continue

                    # Make sure tok1 and tok2 have compatible formats
                    tok2_tax = self.token_vocab[tok2]
                    tok2_avs = self.av_stats.token_avs[tok2]
                    tok2_av_count = self.av_parser.get_av_count(tok2, tok2_avs)
                    if tok2_tax not in [FAM, UNK]:
                        continue

                    # Make sure that both of the tokens are a FAM token used by
                    # at least T AVs (or is a known canonical token)
                    if (tok1 not in self.known_canonical_tokens and
                        tok2 not in self.known_canonical_tokens and
                        tok1_av_count < T and (tok2_tax == UNK or
                                               tok2_av_count < T)):
                        continue

                    # co_occur_pct() is expensive, so this is a heuristic for
                    # skipping any tokens that definitely aren't related
                    tok2_count = self.get_total_count(tok2)
                    min_count, max_count = sorted([tok1_count, tok2_count])
                    if min_count < T:
                        continue
                    if min_count / max_count <= S:
                        continue

                    # Get scan IDs that tok1 occurs in, if we haven't already
                    if not len(tok1_scans):
                        tok1_av_labels = self.av_stats.token_av_labels[tok1]
                        for av, labels in tok1_av_labels.items():
                            for label in labels:
                                idxs = self.av_stats.av_label_scans[av][label]
                                tok1_scans.update(idxs)

                    # Get scan IDs that tok2 occurs in
                    tok2_scans = set()
                    tok2_av_labels = self.av_stats.token_av_labels[tok2]
                    for av, labels in tok2_av_labels.items():
                        for label in labels:
                            idxs = self.av_stats.av_label_scans[av][label]
                            tok2_scans.update(idxs)

                    # If strong co-occurrence percentage is greater than S,
                    # then tok1 and tok2 are sibling aliases
                    strong_co_occur_pct = self.co_occur_pct(tok1_scans,
                                                            tok2_scans)
                    if strong_co_occur_pct >= S:
                        self.resolve_alias_pair(tok1, tok2, FAM)
                        num_resolved += 1

            total_resolved += num_resolved


    def resolve_child_aliases(self, tax, E=0.5, C=0.6):
        """Resolves 'parent/child' aliases.

        Due to differences in granualirity, one token may have a one-way
        relationship with another token. By this, we mean that one token (which
        we call a child token) is less common than a second token (the parent
        token), and the parent token almost always co-occurs in scan reports
        containing the child token. However, since the parent token is more
        widespread, there are scan reports where it occurs but the child
        token does not.

        We identify parent/child aliases as pairs of tokens with high weak
        co-occurrence percentage and low token edit percent.

        Arguments:
        tax -- The type of token to resolve aliases for
        E -- Threshold for edit percent
        C -- Threshold for combined weak co-occurrence percentage and edit
             percentage, (1 - edit_pct) * weak_co_occur_pct
        """

        # Sort tokens by count (largest -> smallest)
        # Give priority to known canonical tokens
        known_canonical = self.known_canonical_tokens[tax]
        unknown_tokens = [tok for tok in self.av_stats.tax_tokens[tax]
                          if tok not in known_canonical]
        known_canonical = list(known_canonical)
        known_canonical.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        unknown_tokens.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        sorted_tokens = known_canonical + unknown_tokens
        remaining_tokens = set(sorted_tokens)
        if tax in [CAT, FILE]:
            remaining_tokens.update(self.av_stats.tax_tokens[PRE])
        if tax == FAM:
            remaining_tokens.update(self.av_stats.tax_tokens[UNK])

        # Iterate over tokens
        for tok1 in sorted_tokens:
            remaining_tokens.remove(tok1)

            # Initialize set of scan IDs that tok1 occurs in, and compute later
            tok1_scans = set()

            # Iterate over every token known to co-occur with tok1
            for tok2 in self.av_stats.related_tokens[tok1]:
                if tok2 not in remaining_tokens:
                    continue

                # Compute edit percentage between tok1 and tok2
                edit_pct = self.edit_pct(tok1, tok2)
                if edit_pct >= E:
                    continue

                # Get scan IDs that tok1 occurs in, if we haven't already
                if not len(tok1_scans):
                    tok1_av_labels = self.av_stats.token_av_labels[tok1]
                    for av, labels in tok1_av_labels.items():
                        for label in labels:
                            idxs = self.av_stats.av_label_scans[av][label]
                            tok1_scans.update(idxs)

                # Get scan IDs that tok2 occurs in
                tok2_scans = set()
                tok2_av_labels = self.av_stats.token_av_labels[tok2]
                for av, labels in tok2_av_labels.items():
                    for label in labels:
                        idxs = self.av_stats.av_label_scans[av][label]
                        tok2_scans.update(idxs)

                # Use a combination of edit pct and co-occurrence percent for
                # identifying parent/child aliases
                weak_co_occur_pct = self.co_occur_pct(tok1_scans, tok2_scans,
                                                      pct_type="weak")
                if (1 - edit_pct) * weak_co_occur_pct >= C:
                    self.child_aliases[tok1].add(tok2)
                    self.parent_aliases[tok2].add(tok1)

        return


    def get_tax_alias_mapping(self, tax, E=0.6):
        """Returns dict where the key is the canonical (most common) name of a
        token, and the value is a list of its aliases.

        Arguments:
        tax -- The type of tokens to resolve aliases for
        E -- Threshold based on edit score and co-occurrence percentage
        """

        # Sort tokens by count (largest -> smallest)
        # Give priority to known canonical tokens
        known_canonical = self.known_canonical_tokens[tax]
        unknown_tokens = [tok for tok in self.av_stats.tax_tokens[tax]
                          if tok not in known_canonical]
        known_canonical = list(known_canonical)
        known_canonical.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        unknown_tokens.sort(key=lambda f: self.av_stats.token_counts[f],
                          reverse=True)
        sorted_tokens = known_canonical + unknown_tokens
        remaining_tokens = set(sorted_tokens)

        # Iterate over all tokens
        tax_alias_mapping = {}
        for tok1 in sorted_tokens:
            if tok1 not in remaining_tokens:
                continue
            remaining_tokens.remove(tok1)

            # Form queue from current token's aliases and child aliases
            alias_queue = self.token_aliases[tok1]
            alias_queue = alias_queue.union(self.child_aliases[tok1])
            alias_queue = list(alias_queue)

            # Recursively get all children of the canonical token
            aliases = set()
            while len(alias_queue):
                tok2 = alias_queue.pop(0)
                if tok2 not in remaining_tokens or tok2 in aliases:
                    continue

                # Don't expand tok2 if it (or its aliases) have a different
                # canonical token
                has_different_canonical = False
                for tok in self.token_aliases[tok2]:
                    if (self.tax_alias_mapping[tax].get(tok) is not None and
                    self.tax_alias_mapping[tax][tok] != tok1):
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
                       if self.tax_alias_mapping[tax].get(tok) is None]
            tax_alias_mapping[tok1] = sorted(aliases)

        return tax_alias_mapping


    def write_alias_mapping(self, alias_file):
        """Write the generated alias mapping to alias_file.

        Arguments:
        alias_file -- A path to the file to write the alias mapping to
        """

        write_taxs = [FAM, GRP, CAT, FILE, PACK]
        with open(alias_file, "w") as f:
            for tax in write_taxs:
                f.write("[{}]\n".format(tax))
                sorted_tax_aliases = list(self.tax_alias_mapping[tax].items())
                sorted_tax_aliases.sort(key=lambda l:l[1])
                for alias, canonical_token in sorted_tax_aliases:
                    f.write("{}\t{}\n".format(alias, canonical_token))
                f.write("\n")
        return
