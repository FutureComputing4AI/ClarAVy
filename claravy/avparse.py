import re
import sys
import json
import math
import string
import logging
import numpy as np
from importlib import import_module
from claravy.taxonomy import *

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("ClarAVy")


class AVParse():

    def __init__(self, av_path, ignore_path, vote_thresholds, hash_format):
        """Class for parsing AV scan data

        Arguments:
        av_path -- Path to file which lists supported AVs.
        ignore_path -- Path to file with user-defined tokens to ignore.
        vote_thresholds -- Dict of vote thresholds for each vocab type.
        hash_format -- The hash format to use (MD5, SHA-1, or SHA-256).
        """

        # Regular expressions used for normalization and parsing
        self.AV_NORM = re.compile(r"\W+")
        self.TOKEN_SPLIT = re.compile(r"[^0-9a-zA-Z]+")
        self.TOKEN_REPLACE = re.compile(r"([0-9a-zA-Z]+)")
        self.TOKEN_RNUM = re.compile(r"^[^0-9]+[0-9]{1,2}$")
        self.CVE_FOUR_RNUM = re.compile(r"^cve[0-9]{4}$")
        self.CVE_MULTI_RNUM = re.compile(r"^cve[0-9]{8,9}$")
        self.MS_RNUM = re.compile(r"^ms[0-9]{2}$")
        self.APT_TOK = re.compile(r"^apt[0-9]+$")
        self.UNC_TOK = re.compile(r"^unc[0-9]+$")
        self.TA_TOK = re.compile(r"^ta[0-9]+$")
        self.FIN_TOK = re.compile(r"^fin[0-9]+$")
        self.MIN_AV_USAGE = 3
        self.vote_thresholds = vote_thresholds
        self.hash_format = hash_format
        self.track_taxs = {FAM, GRP, CAT, FILE, VULN, PACK}
        self.new_fam_tokens = set()
        self.vocab_updated = False

        # Read from configuration files
        av_info = self.read_avs(av_path)
        self.supported_avs, self.correlated_avs, self.av_weights = av_info
        self.ignorelist = self.read_ignorelist(ignore_path)

        # Load parsers for each AV product
        av_modules = {av: "claravy.parsers.parse_{}".format(av)
                      for av in self.supported_avs}
        parser_classes = {av: "Parse_{}".format(av.capitalize())
                          for av in self.supported_avs}
        self.av_parsers = {av: getattr(import_module(av_modules[av]),
                                       parser_classes[av])
                           for av in sorted(self.supported_avs)}

    def normalize_av(self, av):
        """Returns normalized version of AV product name (converted to
        lowercase, non-alphanumeric characters replaced with '_').

        Arguments:
        av -- Unnormalized name of AV product
        """
        return re.sub(self.AV_NORM, "", av).lower().strip()


    def read_avs(self, av_path):
        """Parses file which lists supported AVs.

        Arguments:
        av_path -- Path to file containing names of supported AV products

        Returns:
        supported_avs - set of supported AV products
        correlated_avs - dict mapping each AV to a set of related AV products
        av_weights - weights of AV products for SparseIBCC
        """

        # Read AVs from av_path
        with open(av_path, "r") as f:
            av_info = json.loads(f.read())
        supported_avs = set(av_info.keys())

        # Extend correlated AVs to a depth of 2
        correlated_avs = {}
        for start_av in supported_avs:
            av_set = {av for av in av_info[start_av]["corr_avs"]}
            for next_av in list(av_set):
                av_set.update({av for av in av_info[next_av]["corr_avs"]})
            av_set.add(start_av)
            correlated_avs[start_av] = av_set

        # Get AV weights
        av_weights = []
        for av in sorted(supported_avs):
            av_weights.append(av_info[av]["av_weight"])
        return supported_avs, correlated_avs, av_weights


    def get_av_count(self, tok, tok_avs):
        """Count the number of uncorrelated AV products which are known to
        have used the given token in their labels. Uses the list of correlated
        AV products from read_avs().

        Arguments:
        tok -- A token
        tok_avs -- The AV products which have used that token in their labels.
        """
        av_count = 0
        skip_avs = set()
        for cur_av in tok_avs:
            if cur_av in skip_avs:
                continue
            corr_avs = self.correlated_avs[cur_av]
            skip_avs.update(corr_avs)
            av_count += 1
        return av_count


    def read_vocab(self, tax_path):
        """Read vocab for known tokens into a dict.

        Arguments:
        tax_path -- Path to text file containing the token taxonomy.
        """

        token_vocab = {}
        with open(tax_path, "r") as f:
            cur_vocab = None
            for line in f:
                line = line.split()
                if len(line) != 1:
                    continue
                contents = line[0]
                if contents.startswith("["):
                    cur_vocab = contents[1:-1]
                else:
                    token_vocab[contents] = cur_vocab

        return token_vocab


    def update_vocab(self, av_stats, token_vocab):
        """Updates token vocab mapping after computing stats.

        Arguments:
        av_stats -- AVStats object
        token_vocab -- Dict storing the current token taxonomy
        """

        # Track number of non-correlated AVs that use each token
        token_av_counts = {}

        # Allowable vocab assignment combinations
        tax_tups = {
            (FAM, UNK): FAM,
            (CAT, UNK): CAT,
            (CAT, PRE, UNK): CAT,
            (FILE, UNK): FILE,
            (PRE, FILE, UNK): FILE,
            (PRE, SUF): PRE,
            (PRE, UNK): PRE,
            (PRE, SUF, UNK): PRE,
            (HEUR, UNK): HEUR,
            (HEUR, SUF): HEUR,
            (HEUR, UNK, SUF): HEUR,
            (SUF, UNK): SUF,
        }

        # Override vocab for certain tokens
        for tok, tax_counts in av_stats.token_tax_counts.items():
            if token_vocab.get(tok) is not None:
                continue
            if tok.isnumeric():
                continue

            # Ignore rare vocab assignments
            total_count = sum(tax_counts.values())
            threshold = total_count / 100
            tax_tup = tuple(sorted([tax for tax, count in tax_counts.items()
                                    if count > threshold]))

            # Count number of non-correlated AVs that use tok
            tok_av_count = 0
            if av_stats.token_avs.get(tok) is not None:
                tok_avs = av_stats.token_avs[tok]
                tok_av_count = self.get_av_count(tok, tok_avs)
            token_av_counts[tok] = tok_av_count

            # Assign token taxonomy based on the below checks:
            # Empty tokens -> NULL
            if not len(tok):
                token_vocab[tok] = NULL

            # Handle tokens with unanimous vocab assignments
            elif len(tax_tup) == 1:
                if tax_tup[0] == FAM:
                    if tok_av_count >= self.MIN_AV_USAGE:
                        token_vocab[tok] = FAM
                    else:
                        token_vocab[tok] = UNK
                else:
                    token_vocab[tok] = tax_tup[0]

            # Handle tokens with allowed vocab assignent patterns
            elif tax_tups.get(tax_tup) is not None:
                if tax_tups[tax_tup] == FAM:
                    if tok_av_count >= self.MIN_AV_USAGE:
                        token_vocab[tok] = FAM
                    else:
                        token_vocab[tok] = UNK
                else:
                    token_vocab[tok] = tax_tups[tax_tup]

            # Remaining short tokens are assigned UNK
            elif len(tok) <= 4:
                token_vocab[tok] = UNK

            # Handle remaining possible FAM tokens
            elif tax_counts.get(FAM) is not None:
                if len(tok) <= 2:
                    token_vocab[tok] = UNK
                elif sum(c.isdigit() for c in tok) / len(tok) >= 0.5:
                    token_vocab[tok] = UNK
                elif tax_counts[FAM] / total_count >= 0.5:
                    if tok_av_count >= self.MIN_AV_USAGE:
                        token_vocab[tok] = FAM
                    else:
                        token_vocab[tok] = UNK
                else:
                    token_vocab[tok] = UNK

            # Remaining tokens are unknown
            else:
                token_vocab[tok] = UNK

            # Track all of the new tokens we assigned FAM to
            if token_vocab[tok] == FAM:
                if len(tok) < 4:
                    token_vocab[tok] = UNK
                else:
                    self.new_fam_tokens.add(tok)

        self.vocab_updated = True
        return token_vocab, token_av_counts


    def write_vocab(self, vocab_file, token_vocab):
        """Write the token vocab to vocab_file"""

        # Invert the token taxonomy
        write_taxs = [FAM, GRP, CAT, FILE, PACK, PRE, HEUR]
        vocab_rev = {tax: set() for tax in write_taxs}
        for tok, tax in token_vocab.items():
            if vocab_rev.get(tax) is None:
                continue
            vocab_rev[tax].add(tok)

        # Write token taxonomy to file
        with open(vocab_file, "w") as f:
            for tax in write_taxs:
                f.write("[{}]\n".format(tax))
                tax_tokens = sorted(vocab_rev[tax])
                for tok in tax_tokens:
                    f.write("{}\n".format(tok))
                f.write("\n")
        return


    def update_av_heur_labels(self, av_heur_labels):
        """Update mapping from AV products to likely heuristic labels used by
        those AV products.

        Arguments:
        av_heur_labels -- Dict mapping AV products to heuristic labels.
        """
        self.av_heur_labels = av_heur_labels


    def read_aliases(self, alias_path, token_vocab):
        """
        Reads known aliases for tokens from file.

        Arguments:
        alias_path -- Path to text file containing aliases
        token_vocab -- Dict storing token taxonomy assignments for tokens
        """

        alias_mapping = {}
        cur_vocab = None
        with open(alias_path, "r") as f:
            for line in f:
                line = line.strip()
                if not len(line):
                    continue
                if line.startswith("["):
                    cur_vocab = line[1:-1]
                    continue
                split_line = line.split("\t")
                if len(split_line) != 2:
                    logger.warning("Unable to parse: {}".format(split_line))
                    continue
                alias, canonical_tok = split_line

                # Check that alias matches the token vocab
                if token_vocab.get(alias) is None:
                    token_vocab[alias] = cur_vocab
                elif token_vocab[alias] != cur_vocab:
                    msg = "An alias conflicts with token taxonomy: {} -> {}"
                    logger.warning(msg.format(alias, canonical_tok))
                    continue

                # Check that canonical token matches the token vocab
                if token_vocab.get(canonical_tok) is None:
                    token_vocab[canonical_tok] = cur_vocab
                elif token_vocab[canonical_tok] != cur_vocab:
                    msg = "An alias conflicts with token taxonomy: {} -> {}"
                    logger.warning(msg.format(alias, canonical_tok))
                    continue

                # Add entry to alias mapping
                alias_mapping[alias] = canonical_tok

        return token_vocab, alias_mapping


    def read_ignorelist(self, ignore_file):
        """Read list of ignored tokens from file. These tokens will never be
        output in the token ranking.

        Arguments:
        ignore_file -- Path to file which lists ignored tokens
        """
        ignorelist = set()
        with open(ignore_file, "r") as f:
            for line in f:
                ignorelist.add(line.strip())
        return ignorelist


    def tokenize(self, label):
        """Returns list of tokens from AV label."""
        tokens = re.split(self.TOKEN_SPLIT, label)
        return [tok.lower() for tok in tokens]


    def get_delim_format(self, label):
        """Returns the delimiter format of an AV label. For example, for the AV
        label 'Exploit:Win32/MS08067.xyz', the delimiter format would be
        TOK:TOK/TOK.TOK."""
        return self.TOKEN_REPLACE.sub("TOK", label)


    def replace_known_anno(self, tokens, annos, token_vocab):
        """Returns the annotations for an AV label, with replacements for
        tokens whose annotations are defined in the wordlist.

        Arguments:
        tokens -- A list of tokens for an AV label
        annos -- The annotations for the tokens, prior to replacement
        token_vocab -- Dict storing known vocabs for tokens
        """

        # Replace annotations for hard-coded tokens in wordlist
        for i, tok in enumerate(tokens):

            if not len(tok):
                annos[i] = NULL
                continue

            # Matches CVE patterns split across multiple tokens
            if (tok == "cve" and i < len(tokens) - 2 and
                tokens[i+1].isnumeric() and tokens[i+2].isnumeric()):
                annos[i:i+3] = [VULN, VULN, VULN]
                continue
            if (i < len(tokens) - 1 and tokens[i+1].isnumeric() and
                  re.match(self.CVE_FOUR_RNUM, tok)):
                annos[i:i+2] = [VULN, VULN]
                continue
            if len(tok) >= 11 and re.match(self.CVE_MULTI_RNUM, tok):
                annos[i] = VULN
                continue

            # Match MS pattern
            if (i < len(tokens) - 1 and re.match(self.MS_RNUM, tok) and
                  tokens[i+1].isnumeric()):
                annos[i:i+2] = [VULN, VULN]
                continue

            # Exact match in wordlist
            if token_vocab.get(tok) is not None and token_vocab[tok] != UNK:
                annos[i] = token_vocab[tok]
                continue

            # Identify definite HEUR tokens
            if tok.startswith("generic"):
                annos[i] = HEUR
                continue
            if tok.endswith("generic"):
                annos[i] = HEUR
                continue

            # Identify tokens with threat group naming patterns
            if tok[-1].isnumeric and (annos[i] == FAM or
                                      annos[i] == UNK):
                if re.match(self.APT_TOK, tok):
                    annos[i] = GRP
                    continue
                if re.match(self.UNC_TOK, tok):
                    annos[i] = GRP
                    continue
                if re.match(self.TA_TOK, tok):
                    annos[i] = GRP
                    continue
                if re.match(self.FIN_TOK, tok):
                    annos[i] = GRP
                    continue

            # Identify definite SUF tokens
            if annos[i] != VULN and tok.isnumeric():
                annos[i] = SUF
                continue
            if annos[i] != VULN and len(tok) >= 2 and tok[:-1].isnumeric():
                annos[i] = SUF
                continue
            if annos[i] != NULL and len(tok) == 1:
                annos[i] = SUF
                continue
            if annos[i] == UNK and len(tok) <= 3:
                annos[i] = SUF
                continue

            # Like a token in the wordlist and ends in 1-2 digits
            if re.match(self.TOKEN_RNUM, tok):
                tok_rstrip = tok.rstrip(string.digits)
                if (len(tok_rstrip) >= len(tok) - 2 and
                    len(tok_rstrip) >= 4 and
                    token_vocab.get(tok_rstrip) is not None):
                    annos[i] = token_vocab[tok_rstrip]
                    continue

            # Like a token in the wordlist and ends in an extra non-digit token
            if len(tok) >= 7 and token_vocab.get(tok[:-1]) is not None:
                annos[i] = token_vocab[tok[:-1]]
                continue

            # Once we have updated the vocab, any remaining FAM tokens are
            # replaced with UNK
            if (self.vocab_updated and annos[i] == FAM and
                token_vocab.get(tok) is not None and token_vocab[tok] != FAM):
                annos[i] = UNK

        return annos


    def replace_vuln_tokens(self, vuln_tokens):
        """Combines and normalizes VULN tokens if they are split up.

        Arguments:
        vuln_tokens -- A list of (possibly split) VULN tokens
        """

        # No VULN tokens to handle
        if not len(vuln_tokens):
            return []

        # cve_####_####
        elif len(vuln_tokens) == 3:
            vuln_tokens = ["_".join(vuln_tokens)]
        elif len(vuln_tokens) == 4:
            vuln_tokens = ["_".join(vuln_tokens[:3])]

        # Two CVEs in same label
        elif (len(vuln_tokens) == 6 and vuln_tokens[0] == "cve" and
              vuln_tokens[3] == "cve"):
            vuln_tokens = ["_".join(vuln_tokens[:3]),
                           "_".join(vuln_tokens[3:])]

        # cve_######## -> cve_####_####
        elif (len(vuln_tokens) == 2 and vuln_tokens[0].startswith("cve") and
              vuln_tokens[0][3:].isnumeric()):
            vuln_tok = "cve_{}_{}".format(vuln_tokens[0][3:], vuln_tokens[1])
            vuln_tokens = [vuln_tok]

        # ms_####
        elif (len(vuln_tokens) == 2 and vuln_tokens[0].startswith("ms") and
              vuln_tokens[1].isnumeric()):
            vuln_tokens = ["_".join(vuln_tokens)]

        # cve######## -> cve_####_####
        elif len(vuln_tokens) == 1:
            vuln_tok = vuln_tokens[0]
            if 8 <= len(vuln_tok) <= 9 and vuln_tok[:2] == "20":
                year = vuln_tok[:4]
                cve_num = vuln_tok[4:]
                vuln_tok = "cve_{}_{}".format(year, cve_num)
                vuln_tokens = [vuln_tok]
            elif (vuln_tok.startswith("cve") and len(vuln_tok) >= 11 and
                  vuln_tok[3:].isnumeric()):
                vuln_tok = "cve_{}_{}".format(vuln_tok[3:7], vuln_tok[7:])
                vuln_tokens = [vuln_tok]

        return vuln_tokens


    def get_anno_format(self, label, av, token_vocab, alias_mapping={}):
        """Returns annotated format from AV label.

        Arguments:
        label -- AV label
        av -- normalized AV product name
        token_vocab -- Dict storing known vocabs for tokens
        alias_mapping -- Dict mapping aliases to canonical tokens
        """

        # Tokenize AV label and get delimiter format
        tokens = self.tokenize(label)
        delim_fmt = self.get_delim_format(label)

        # Try to find parsing rule based on AV and delimiter format
        parser = self.av_parsers[av]()
        parse_rule = parser.parse_delim_fmt.get(delim_fmt)

        # Default annotated format is all UNK (if no parsing rule was found)
        annos = [UNK]*len(tokens)

        # If a parsing rule was found, can annotate the label
        if parse_rule is not None:
            annos = parse_rule(tokens)

        # Resolve aliases if alias_mapping is provided
        if alias_mapping:
            for i, tok in enumerate(tokens):
                if alias_mapping.get(tok) is not None:
                    tokens[i] = alias_mapping[tok]

        # Update annotated format with wordlist, global rules
        annos = self.replace_known_anno(tokens, annos, token_vocab)
        return tokens, annos


    def load_report(self, report_json):
        """Loads a scan report from a JSON string, performs validation, and
        returns it in a standardized format.

        Arguments:
        report_json -- JSON string for the report, in VirusTotal API format.
        """

        # Attempt to parse JSON string
        if report_json is None:
            return []
        is_valid = True
        report = []
        try:
            report = json.loads(report_json)
        except (json.decoder.JSONDecodeError, UnicodeDecodeError):
            is_valid = False

        # Check that contents of scan report is valid
        if not len(report):
            is_valid = False
        elif not isinstance(report, dict):
            is_valid = False
        if not is_valid:
            return {}

        # Handle vt-v3 scans
        if report.get("data") is not None:
            report = report["data"]
            if report.get("attributes") is not None:
                report = report["attributes"]
            else:
                is_valid = False

        # Handle vt-v2 scans
        elif report.get("scans") is None:
            is_valid = False
        if report.get(self.hash_format) is None:
            is_valid = False
        if not is_valid:
            return {}

        # Re-organize report in standardized format
        loaded_report = {
            "md5": report["md5"],
            "sha1": report["sha1"],
            "sha256": report["sha256"],
            "scans": {},
            "n_scans": 0,
        }

        # Parse scans from report
        scans = None
        if report.get("last_analysis_results") is not None:
            scans = report["last_analysis_results"]
        else:
            scans = report["scans"]

        # Gather AV labels
        for av, scan in scans.items():
            av = self.normalize_av(av)
            if av not in self.supported_avs:
                continue
            loaded_report["n_scans"] += 1
            if scan.get("result") is None:
                continue
            label = scan["result"]
            if not len(label):
                continue
            loaded_report["scans"][av] = label

        return loaded_report


    def report_stats(self, report, token_vocab):
        """Returns a loaded AV scan report in a format which can be used to
        compute stats about its contents by an AVStats object. The return
        value is in the format:

        (md5, [(av, label, [(tok, tax)])])

        Arguments:
        report -- Dict containing AV scan report in VirusTotal API format
        token_vocab -- Dict storing known vocabs for tokens
        """

        if not len(report):
            return []
        md5 = report["md5"]
        av_results = []
        for av, label in report["scans"].items():
            tokens, annos = self.get_anno_format(label, av, token_vocab)
            av_results.append((av, label, zip(tokens, annos)))
        return (md5, av_results)


    def process_batch(self, batch, token_vocab, alias_mapping):
        """Parses a list of JSON objects representing VirusTotal scan reports,
        and returns lists of the following for each scan report

        hashes -- The md5, sha1, or sha256 for each file in the batch
        tags -- tag ranking for each report in the batch
        families -- family votes from each AV, for each report in the batch
        features -- feature vector used for computing confidence score
        detections -- number of AV products which detect each file as malware

        Arguments:
        batch -- List of VirusTotal reports in JSON format
        token_vocab -- Dict storing known vocabs for tokens
        alias_mapping -- Dict mapping aliases to canonical tokens
        """

        i = 0
        hashes = []
        tags = []
        families = []
        features = []
        detections = []
        for report_json in batch:
            report = self.load_report(report_json)
            if not report:
                continue
            file_hash = report[self.hash_format]
            tax_token_avs = {tax: {} for tax in self.track_taxs}
            av_norm_labels = {}

            for av, label in report["scans"].items():
                tokens, annos = self.get_anno_format(label, av, token_vocab,
                                                        alias_mapping)
                tax_tokens = {tax: [] for tax in self.track_taxs}
                norm_label = []
                for i, tok in enumerate(tokens):
                    tax = annos[i]
                    if tax != SUF:
                        norm_label.append(tok)
                    if tax not in self.track_taxs:
                        continue
                    tax_tokens[tax].append(tok)
                norm_label = ".".join(norm_label)
                is_heur = False
                if norm_label in self.av_heur_labels[av]:
                    is_heur = True
                tax_tokens[VULN] = self.replace_vuln_tokens(tax_tokens[VULN])
                for tax, tokens in tax_tokens.items():
                    for tok in tokens:
                        if tax == FAM and is_heur:
                            continue
                        if tax_token_avs[tax].get(tok) is None:
                            tax_token_avs[tax][tok] = set()
                        tax_token_avs[tax][tok].add(av)

            # Get tag rankings for non-FAM tokens
            tag_ranking = []
            for tax in self.track_taxs:
                if tax == FAM:
                    continue

                # Score is number of votes from non-correlated AVs
                token_scores = {}
                for tok, avs in tax_token_avs[tax].items():
                    token_scores[tok] = self.get_av_count(tok, avs)

                # Skip tokens that do not have a sufficient vote
                for tok, score in token_scores.items():
                    if tok in self.ignorelist:
                        continue
                    if score < self.vote_thresholds[tax]:
                        continue
                    tag_ranking.append(("{}:{}".format(tax, tok), score))

            # Format tag ranking for output
            tag_ranking.sort(key=lambda l:l[1], reverse=True)
            tag_ranking = ["{}|{}".format(tok, count)
                           for tok, count in tag_ranking]
            if not len(tag_ranking):
                tag_ranking = []
            tag_ranking = ",".join(tag_ranking)

            # Compute features about scan report
            n_fams = len(tax_token_avs[FAM])
            n_fam_labels = sum([len(avs) for avs in
                                tax_token_avs[FAM].values()])
            n_detect = len(report["scans"])
            n_scan = report["n_scans"]
            fam_entropy = 0.0
            for avs in tax_token_avs[FAM].values():
                p_fam = len(avs) / n_fam_labels
                log_p_fam = 0.0
                if n_fams > 1:
                    log_p_fam = math.log(p_fam, n_fams)
                fam_entropy -= p_fam * log_p_fam

            # Append info extracted from this scan report
            hashes.append(file_hash)
            tags.append(tag_ranking)
            families.append(tax_token_avs[FAM])
            features.append([
                n_fams,
                fam_entropy,
                n_detect / n_scan if n_scan > 0 else 0,
                n_fam_labels / n_detect if n_detect > 0 else 0,
                n_fam_labels / n_scan if n_scan > 0 else 0,
                0, # Will become probability of most likely family
                0, # Will become entropy of predicted probabilities
            ])
            detections.append("{}/{}".format(n_detect, n_scan))

        features = np.array(features)
        return hashes, tags, families, features, detections
