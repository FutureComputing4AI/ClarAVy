import numpy as np
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

        self.valid_alias_taxs = {FAM, CAT, FILE, PRE, UNK}
        self.valid_fam_taxs = {FAM, UNK}
        self.valid_cat_taxs = {CAT, PRE, UNK}
        self.valid_tgt_taxs = {FILE, PRE, UNK}
        self.ignore_av_taxs = {SUF, HEUR, NULL}
        self.num_scans = 0

        self.av_heur_labels = {av: set() for av in supported_avs}
        self.av_label_scans = {av: {} for av in supported_avs}
        self.av_label_tokens = {av: {} for av in supported_avs}

        self.related_tokens = {}
        self.related_av_labels = {av: {} for av in supported_avs}
        self.token_tax_counts = {}
        self.token_avs = {}
        self.token_av_counts = {}


    def update_stats(self, stats):
        scan_id = self.num_scans
        self.num_scans += 1

        fam_toks = set()
        cat_toks = set()
        tgt_toks = set()
        fam_labels = set()
        for av, label, tok_taxs in stats[1]:

            # Update stats for tokens
            tok_taxs = list(tok_taxs)
            tokens_norm = []
            is_fam = False
            is_heur = False
            for tok, tax in tok_taxs:

                # Check if token has been seen before
                if self.token_tax_counts.get(tok) is None:
                    self.token_tax_counts[tok] = {tax: 0}
                    self.related_tokens[tok] = set()

                # Track how many times a tax has been assigned to the token
                if self.token_tax_counts[tok].get(tax) is None:
                    self.token_tax_counts[tok][tax] = 0
                self.token_tax_counts[tok][tax] += 1

                # Track which AVs have used this token
                if tax not in self.ignore_av_taxs:
                    if self.token_avs.get(tok) is None:
                        self.token_avs[tok] = set()
                    self.token_avs[tok].add(av)

                    if self.token_av_counts.get(tok) is None:
                        self.token_av_counts[tok] = {}
                    if self.token_av_counts[tok].get(av) is None:
                        self.token_av_counts[tok][av] = 0
                    self.token_av_counts[tok][av] += 1

                # Track FAM, CAT, and FILE tokens
                if tax in self.valid_fam_taxs:
                    fam_toks.add((av, tok, tax))
                if tax in self.valid_cat_taxs:
                    cat_toks.add((av, tok, tax))
                if tax in self.valid_tgt_taxs:
                    tgt_toks.add((av, tok, tax))

                # Identify labels with heuristic tokens or family tokens
                if tax == HEUR:
                    is_heur = True
                elif tax == FAM:
                    is_fam = True

                # Construct normalized label
                # UNK tokens after the family are likely SUF tokens
                if tax == SUF or (is_fam and tax == UNK):
                    tokens_norm.append(SUF)
                elif tax == NULL:
                    tokens_norm.append(NULL)
                else:
                    tokens_norm.append(tok)

            # Normalize label
            label_norm = ".".join(tokens_norm)
            if self.av_label_scans[av].get(label_norm) is None:
                self.av_label_scans[av][label_norm] = set()
                if len(tokens_norm):
                    self.av_label_tokens[av][label_norm] = tokens_norm
            self.av_label_scans[av][label_norm].add(scan_id)

            # Track heuristic and family labels
            if is_heur:
                self.av_heur_labels[av].add(label_norm)
            elif is_fam:
                fam_labels.add((av, label_norm))

        # Update related FAM tokens for current report
        for av1, tok1, tax1 in fam_toks:
            if tax1 != FAM:
                continue
            for av2, tok2, _ in fam_toks:
                if av1 == av2:
                    continue
                self.related_tokens[tok1].add(tok2)

        # Update related CAT tokens for current report
        for av1, tok1, tax1 in cat_toks:
            if tax1 != CAT:
                continue
            for av2, tok2, _ in cat_toks:
                if av1 == av2:
                    continue
                self.related_tokens[tok1].add(tok2)

        # Update related FILE tokens for current report
        for av1, tok1, tax1 in tgt_toks:
            if tax1 != FILE:
                continue
            for av2, tok2, _ in tgt_toks:
                if av1 == av2:
                    continue
                self.related_tokens[tok1].add(tok2)

        # Track related labels with FAM tokens and without HEUR tokens
        if len(fam_labels) == 1:
            return
        for label_tup in fam_labels:
            av, label = label_tup
            if self.related_av_labels[av].get(label) is None:
                self.related_av_labels[av][label] = set()
            self.related_av_labels[av][label] = fam_labels - set([label_tup])

        return


class AVStats:

    def __init__(self, supported_avs):
        """Class for computing and storing stats about AV scan reports.

        Arguments:
        supported_avs -- List of supported AV products.
        """

        # Updated by calling reduce_stats
        self.num_scans = 0
        self.supported_avs = supported_avs
        self.token_tax_counts = {}
        self.token_avs = {}
        self.token_av_counts = {}
        self.related_tokens = {}
        self.related_av_labels = {av: {} for av in supported_avs}
        self.av_labels = {av: set() for av in supported_avs}
        self.av_label_idxs = {av: {} for av in supported_avs}
        self.av_idx_labels = {av: [] for av in supported_avs}
        self.av_heur_labels = {av: set() for av in supported_avs}
        self.av_label_scans = {av: {} for av in supported_avs}
        self.av_label_tokens = {av: {} for av in supported_avs}

        # Updated by calling update_token_stats
        self.tax_tokens = None
        self.token_counts = None
        self.token_av_labels = None


    def reduce_stats(self, mapper):
        """Update stats using an AVStats mapper.

        Arguments:
        mapper - an AVStats_Map object
        """

        # Reduce AV labels
        for av in mapper.av_label_scans.keys():
            for label in mapper.av_label_scans[av].keys():

                # Handle new AV labels
                if label not in self.av_labels[av]:
                    self.av_label_idxs[av][label] = len(self.av_labels[av])
                    self.av_labels[av].add(label)
                    self.av_idx_labels[av].append(label)

                # Map label IDs -> scan IDs
                label_idx = self.av_label_idxs[av][label]
                scan_idxs = {self.num_scans + idx
                             for idx in mapper.av_label_scans[av][label]}
                if self.av_label_scans[av].get(label_idx) is None:
                    self.av_label_scans[av][label_idx] = scan_idxs
                else:
                    self.av_label_scans[av][label_idx].update(scan_idxs)

                # Handle heuristic labels
                if label in mapper.av_heur_labels[av]:
                    self.av_heur_labels[av].add(label_idx)

                # Map label IDs -> tokens
                if (mapper.av_label_tokens[av].get(label) is not None and
                    self.av_label_tokens[av].get(label_idx) is None):
                    tokens = mapper.av_label_tokens[av][label]
                    self.av_label_tokens[av][label_idx] = tokens

        # Reduce token FMT counts
        for tok, tax_counts in mapper.token_tax_counts.items():
            if self.token_tax_counts.get(tok) is None:
                self.token_tax_counts[tok] = tax_counts
            else:
                for tax, count in tax_counts.items():
                    if self.token_tax_counts[tok].get(tax) is None:
                        self.token_tax_counts[tok][tax] = count
                    else:
                        self.token_tax_counts[tok][tax] += count

        # Reduce token AV assignments
        for tok, avs in mapper.token_avs.items():
            if self.token_avs.get(tok) is None:
                self.token_avs[tok] = set()
            self.token_avs[tok].update(avs)

        for tok, avs in mapper.token_av_counts.items():
            if self.token_av_counts.get(tok) is None:
                self.token_av_counts[tok] = {}
            for av in avs:
                if self.token_av_counts[tok].get(av) is None:
                    self.token_av_counts[tok][av] = 0
                count = mapper.token_av_counts[tok][av]
                self.token_av_counts[tok][av] += count

        # Reduce related tokens
        for tok, related_toks in mapper.related_tokens.items():
            if self.related_tokens.get(tok) is None:
                self.related_tokens[tok] = related_toks
            else:
                self.related_tokens[tok].update(related_toks)

        # Reduce related labels with FAM tokens and without HEUR tokens
        for av in mapper.related_av_labels.keys():
            for label in mapper.related_av_labels[av].keys():
                label_idx = self.av_label_idxs[av][label]
                related_labels = set()
                related_tups = mapper.related_av_labels[av][label]
                for related_av, related_label in related_tups:
                    related_idx = self.av_label_idxs[related_av][related_label]
                    related_labels.add((related_av, related_idx))
                if self.related_av_labels[av].get(label_idx) is None:
                    self.related_av_labels[av][label_idx] = set()
                self.related_av_labels[av][label_idx].update(related_labels)

        # Update number of scans
        self.num_scans += mapper.num_scans
        return


    def update_token_stats(self, token_vocab, alias_mapping, corr_avs,
                           new_fam_tokens):
        """Calculates stats about each token's appearance in the dataset.
        Initializes stats about tokens in the user-defined taxonomy if they
        are not encountered in the dataset.

        Arguments:
        token_vocab -- Dict storing known vocabs for tokens
        alias_mapping -- Dict mapping aliases to canonical tokens
        corr_avs -- Maps each AV to a set of correlated AV products
        new_fam_tokens -- Set of automatically-identified FAM tokens
        """

        # Now that we have a token taxonomy, we have other stats that need to
        # be updated
        # Map vocab back to tokens, and track stats about tokens
        self.tax_tokens = {
            FAM = set(),
            GRP = set(),
            FILE = set(),
            CAT = set(),
            PACK = set(),
            VULN = set(),
            PRE = set(),
            SUF = set(),
            HEUR = set(),
            UNK = set(),
            NULL = set()
        }
        self.token_counts = {}
        for tok, tax in token_vocab.items():

            # Map vocab -> tokens
            self.tax_tokens[tax].add(tok)

            # Track token counts
            if self.token_tax_counts.get(tok) is None:
                self.token_counts[tok] = 0
            else:
                token_count = sum(self.token_tax_counts[tok].values())
                self.token_counts[tok] = token_count

            # Track token AVs
            if self.token_avs.get(tok) is None:
                self.token_avs[tok] = set()

            # Track related tokens
            if self.related_tokens.get(tok) is None:
                self.related_tokens[tok] = set()

        # Map tokens -> AV label IDs
        self.token_av_labels = {tok: {} for tok in token_vocab.keys()}
        for av in self.av_label_tokens.keys():
            for label, tokens in self.av_label_tokens[av].items():
                for tok in tokens:
                    if self.token_av_labels.get(tok) is None:
                        self.token_av_labels[tok] = {}
                    if self.token_av_labels[tok].get(av) is None:
                        self.token_av_labels[tok][av] = set()
                    self.token_av_labels[tok][av].add(label)

        # From here, only track stats about FAM tokens
        # Get all family tokens and their aliases
        fam_aliases = {}
        for fam in self.tax_tokens[FAM]:
            if alias_mapping.get(fam) is None:
                fam_aliases[fam] = set([fam])
            else:
                canonical_fam = alias_mapping[fam]
                if fam_aliases.get(canonical_fam) is None:
                    fam_aliases[canonical_fam] = set([canonical_fam])
                fam_aliases[canonical_fam].add(fam)

        # Identify other AV labels which are likely to be heuristics
        # These are AV labels that are applied much more widely than other
        # AV labels that detect the same family, and have little agreement
        # with those AV labels
        for aliases in fam_aliases.values():
            av_labels = {}
            scan_sizes = []
            for fam in aliases:
                for av, labels in self.token_av_labels[fam].items():
                    for label in labels:
                        if label in self.av_heur_labels[av]:
                            continue
                        if av_labels.get(av) is None:
                            av_labels[av] = set()
                        av_labels[av].add(label)
                        scans = self.av_label_scans[av][label]
                        scan_sizes.append(len(scans))
            scan_sizes = np.array(scan_sizes)
            if not len(scan_sizes):
                continue
            median_scan_size = np.median(scan_sizes)

            for av_1, labels_1 in av_labels.items():
                for label_1 in labels_1:
                    scans_1 = self.av_label_scans[av_1][label_1]

                    # Suspicious of AV labels that are over 10x more common
                    # than the median family size - start investigating
                    if len(scans_1) < 100:
                        continue
                    if len(scans_1) < median_scan_size * 10:
                        continue

                    # Compare to other AV labels with the same family
                    num_agree = 0
                    num_labels = 0
                    for av_2, labels_2 in av_labels.items():
                        if av_2 in corr_avs[av_1]:
                            continue
                        for label_2 in labels_2:
                            if label_1 == label_2:
                                continue
                            scans_2 = self.av_label_scans[av_2][label_2]
                            if len(scans_1) < len(scans_2):
                                continue
                            inter = len(scans_1.intersection(scans_2))
                            union = len(scans_1.union(scans_2))
                            if inter / union > 0.1:
                                num_agree += 1
                            num_labels += 1

                        # If we find 3+ other labels that this label rarely
                        # agrees with, then we consider it a heuristic label
                        if num_labels >= 3 and num_agree / num_labels < 0.1:
                            self.av_heur_labels[av_1].add(label_1)

        # Convert av_heur_labels to use normalized labels instead of idxs
        for av in self.av_heur_labels.keys():
            label_idxs = self.av_heur_labels[av]
            labels = [self.av_idx_labels[av][label_idx]
                      for label_idx in label_idxs]
            self.av_heur_labels[av] = labels
