import re
import json
import string
from importlib import import_module
from claravy.taxonomy import *


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
        self.vote_thresholds = vote_thresholds
        self.hash_format = hash_format
        self.track_fmts = set([CAT, TGT, VULN, PACK])

        # Read from configuratio files
        self.supported_avs, self.correlated_avs = self.read_avs(av_path)
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
        """Return normalized version of AV product name (convert to lowercase
        and replace non-alphanumeric characters with '_')

        Arguments:
        av -- name of AV product
        """

        return re.sub(self.AV_NORM, "", av).lower().strip()


    def read_avs(self, av_path):
        """Parses file which lists supported AVs.

        Arguments:
        av_path -- Path to file containing names of AV products, one per line.

        Returns:
        supported_avs - set of supported AV products
        ext_correlated_avs - dict mapping each AV to set of related AV products
        """

        # Read AVs from av_path
        supported_avs = set()
        correlated_avs = {}
        with open(av_path, "r") as f:
            for line in f:
                av, corr_avs = line.strip().split(",")

                # Normalize AV product
                av = self.normalize_av(av)
                supported_avs.add(av)

                # Add AVs that are related to current AV
                corr_avs = [corr_av for corr_av in corr_avs.split("/")
                            if len(corr_av)]
                correlated_avs[av] = set()
                for corr_av in corr_avs:
                    correlated_avs[av].add(self.normalize_av(corr_av))

        # Extend correlated AVs to a depth of 2
        ext_correlated_avs = {}
        for start_av in supported_avs:
            av_set = set([av for av in correlated_avs[start_av]])
            for next_av in list(av_set):
                av_set.update(set([av for av in correlated_avs[next_av]]))
            av_set.add(start_av)
            ext_correlated_avs[start_av] = av_set

        return supported_avs, ext_correlated_avs


    def read_vocab(self, wordlist_path):
        """Read vocab for known tokens into a dict.

        Arguments:
        wordlist_path -- Path to text file containing wordlist. Refer to
                         format of data/default_wordlist.txt
        """

        token_vocab = {}
        with open(wordlist_path, "r") as f:
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
        token_vocab -- Current dict of token vocab assignments
        """

        fmt_tups = {
            (FAM, UNK): FAM,
            (CAT, UNK): CAT,
            (CAT, PRE, UNK): CAT,
            (TGT, UNK): TGT,
            (PRE, TGT, UNK): TGT,
            (PRE, SUF): PRE,
            (PRE, UNK): PRE,
            (PRE, SUF, UNK): PRE
        }

        # Override vocab for certain tokens
        for tok, fmt_counts in av_stats.token_fmt_counts.items():
            if token_vocab.get(tok) is not None:
                continue
            if tok.isnumeric():
                continue

            # Discard rare vocab assignments
            total_count = sum(fmt_counts.values())
            threshold = total_count / 100
            fmt_tup = tuple(sorted([fmt for fmt, count in fmt_counts.items()
                                    if count > threshold]))

            # Assign vocab
            if len(fmt_tup) == 1:
                token_vocab[tok] = fmt_tup[0]
            elif fmt_tups.get(fmt_tup) is not None:
                token_vocab[tok] = fmt_tups[fmt_tup]
            else:
                token_vocab[tok] = UNK
        return token_vocab


    def write_vocab(self, vocab_file, token_vocab):
        """Write the token vocab to vocab_file"""

        # Invert the token vocabulary
        write_fmts = [CAT, TGT, VULN, PACK, PRE]
        vocab_rev = {fmt: set() for fmt in write_fmts}
        for tok, fmt in token_vocab.items():
            if vocab_rev.get(fmt) is None:
                continue
            vocab_rev[fmt].add(tok)

        # Write token vocab to file
        with open(vocab_file, "w") as f:
            for fmt in write_fmts:
                f.write("[{}]\n".format(fmt))
                fmt_tokens = sorted(vocab_rev[fmt])
                for tok in fmt_tokens:
                    f.write("{}\n".format(tok))
                f.write("\n")
        return


    def read_aliases(self, alias_path, token_vocab):
        """
        Reads aliases for known tokens into a dict.

        Arguments:
        alias_path -- Path to text file containing aliases. Refer to format
                      of data/default_aliases.txt
        token_vocab -- Dict storing known vocabs for tokens
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
                if len(line.split("\t")) != 2:
                    continue
                alias, canonical_tok = line.split("\t")

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
        output in the token ranking."""
        ignorelist = set()
        with open(ignore_file, "r") as f:
            for line in f:
                ignorelist.add(line.strip())
        return ignorelist


    def tokenize(self, label):
        """Returns list of tokens from AV label."""
        tokens = re.split(self.TOKEN_SPLIT, label)
        return [tok.lower() for tok in tokens]


    def get_gen_format(self, label):
        """Returns generic format from AV label."""
        return self.TOKEN_REPLACE.sub("TOK", label)


    def replace_known_anno(self, tokens, anno_fmt, token_vocab):
        """Returns the annotated format from an AV label, with replacements
        for tokens whose annotations are defined in the wordlist.

        Arguments:
        tokens -- A list of tokens for an AV label
        anno_fmt -- The annotation format for the tokens, prior to replacement
        token_vocab -- Dict storing known vocabs for tokens
        """

        # Replace annotations for hard-coded tokens in wordlist
        for i, tok in enumerate(tokens):

            # Matches CVE patterns split across multiple tokens
            if (tok == "cve" and i < len(tokens) - 2 and
                tokens[i+1].isnumeric() and tokens[i+2].isnumeric()):
                anno_fmt[i:i+3] = [VULN, VULN, VULN]
                continue
            if (i < len(tokens) - 1 and tokens[i+1].isnumeric() and
                  re.match(self.CVE_FOUR_RNUM, tok)):
                anno_fmt[i:i+2] = [VULN, VULN]
                continue
            if len(tok) >= 11 and re.match(self.CVE_MULTI_RNUM, tok):
                anno_fmt[i] = VULN
                continue

            # Match MS pattern
            if (i < len(tokens) - 1 and re.match(self.MS_RNUM, tok) and
                  tokens[i+1].isnumeric()):
                anno_fmt[i:i+2] = [VULN, VULN]
                continue

            # Exact match in wordlist
            if token_vocab.get(tok) is not None:
                anno_fmt[i] = token_vocab[tok]
                continue

            # Identify definite SUF tokens
            if anno_fmt[i] != VULN and tok.isnumeric():
                anno_fmt[i] = SUF
                continue
            if anno_fmt[i] != NULL and len(tok) == 1:
                anno_fmt[i] = SUF
                continue

            # Like a token in the wordlist and ends in 1-2 digits
            if re.match(self.TOKEN_RNUM, tok):
                tok_rstrip = tok.rstrip(string.digits)
                if (len(tok_rstrip) >= len(tok) - 2 and
                    len(tok_rstrip) >= 4 and
                    token_vocab.get(tok_rstrip) is not None):
                    anno_fmt[i] = token_vocab[tok_rstrip]
                    continue

            # Like a token in the wordlist and ends in an extra non-digit token
            if len(tok) >= 7 and token_vocab.get(tok[:-1]) is not None:
                anno_fmt[i] = token_vocab[tok[:-1]]
                continue

        return anno_fmt


    def replace_vuln_tokens(self, vuln_tokens):
        """Combines and normalizes VULN tokens if they are split up.

        Arguments:
        vuln_tokens -- A list of (possibly split) VULN tokens
        """

        if not len(vuln_tokens):
            return []
        elif len(vuln_tokens) == 3:
            vuln_tokens = ["_".join(vuln_tokens)]
        elif len(vuln_tokens) == 4:
            vuln_tokens = ["_".join(vuln_tokens[:3])]
        elif (len(vuln_tokens) == 6 and vuln_tokens[0] == "cve" and
              vuln_tokens[3] == "cve"):
            vuln_tokens = ["_".join(vuln_tokens[:3]),
                           "_".join(vuln_tokens[3:])]
        elif (len(vuln_tokens) == 2 and vuln_tokens[0].startswith("cve") and
              vuln_tokens[0][3:].isnumeric()):
            vuln_tok = "cve_{}_{}".format(vuln_tokens[0][3:], vuln_tokens[1])
            vuln_tokens = [vuln_tok]
        elif (len(vuln_tokens) == 2 and vuln_tokens[0].startswith("ms") and
              vuln_tokens[1].isnumeric()):
            vuln_tokens = ["_".join(vuln_tokens)]
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
        label -- AV label string
        av -- normalized AV product name
        token_vocab -- Dict storing known vocabs for tokens
        alias_mapping -- Dict mapping aliases to canonical tokens
        """

        # Tokenize AV label and get generic label format
        tokens = self.tokenize(label)
        gen_fmt = self.get_gen_format(label)

        # Try to find parsing rule based on AV and generic format
        parser = self.av_parsers[av]()
        parse_rule = parser.parse_fmt.get(gen_fmt)

        # Default annotated format is all UNK (if no parsing rule was found)
        anno_fmt = [UNK]*len(tokens)

        # If a parsing rule was found, can annotate the label
        if parse_rule is not None:
            anno_fmt = parse_rule(tokens)

        # Resolve aliases if alias_mapping is provided
        if alias_mapping:
            for i, tok in enumerate(tokens):
                if alias_mapping.get(tok) is not None:
                    tokens[i] = alias_mapping[tok]

        # Update annotated format with wordlist, global rules
        anno_fmt = self.replace_known_anno(tokens, anno_fmt, token_vocab)
        return tokens, anno_fmt


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
        }

        # Parse scans from report
        scans = None
        if report.get("last_analysis_results") is not None:
            scans = report["last_analysis_results"]
        else:
            scans = report["scans"]
        
        for av, scan in scans.items():
            av = self.normalize_av(av)
            if av not in self.supported_avs:
                continue
            if scan.get("result") is None:
                continue
            label = scan["result"]
            loaded_report["scans"][av] = label

        return loaded_report


    def report_stats(self, report, token_vocab):
        """Returns a loaded AV scan report in a format which can be used to
        compute stats about its contents. The return value is in the format:

        (md5, [(av, label, [(tok, fmt)])])

        Arguments:
        report -- Dict containing AV scan report in VirusTotal API format
        token_vocab -- Dict storing known vocabs for tokens
        """

        if not len(report):
            return []
        md5 = report["md5"]
        av_results = []
        for av, label in report["scans"].items():
            tokens, anno_fmt = self.get_anno_format(label, av, token_vocab)
            av_results.append((av, label, zip(tokens, anno_fmt)))
        return (md5, av_results)


    def report_ranking(self, report, token_vocab, alias_mapping):
        """Parses a loaded scan report and returns a ranking of tokens for each
        vocab type in (TGT, CAT, PACK, and VULN). Includes an AVClas2-style
        string with the file's hash, the number of AVs that detected the file,
        and the number of votes for each token.

        Arguments:
        report -- Dict containing AV scan report in VirusTotal API format
        token_vocab -- Dict storing known vocabs for tokens
        alias_mapping -- Dict mapping aliases to canonical tokens
        """

        file_hash = report[self.hash_format]
        fmt_token_avs = {fmt: {} for fmt in self.track_fmts}
        for av, label in report["scans"].items():
            tokens, anno_fmt = self.get_anno_format(label, av, token_vocab,
                                                    alias_mapping)
            fmt_tokens = {fmt: [] for fmt in self.track_fmts}
            for i, tok in enumerate(tokens):
                fmt = anno_fmt[i]
                if fmt not in self.track_fmts:
                    continue
                fmt_tokens[fmt].append(tok)
            fmt_tokens[VULN] = self.replace_vuln_tokens(fmt_tokens[VULN])
            for fmt, tokens in fmt_tokens.items():
                for tok in tokens:
                    if fmt_token_avs[fmt].get(tok) is None:
                        fmt_token_avs[fmt][tok] = set()
                    fmt_token_avs[fmt][tok].add(av)

        # Get scores for tokens in each fmt
        ranking = []
        for fmt in self.track_fmts:

            # Get sets of correlated AVs
            token_scores = {}
            for tok, avs in fmt_token_avs[fmt].items():
                skip_avs = set()
                score = 0
                for cur_av in avs:
                    if cur_av in skip_avs:
                        continue
                    corr_avs = self.correlated_avs[cur_av]
                    skip_avs.update(corr_avs)
                    score += 1
                token_scores[tok] = score
            for tok, score in token_scores.items():
                if tok in self.ignorelist:
                    continue
                if score < self.vote_thresholds[fmt]:
                    continue
                ranking.append(("{}:{}".format(fmt, tok), score))

        # Format ranking for output
        ranking.sort(key=lambda l:l[1], reverse=True)
        ranking = ["{}|{}".format(tok, count) for tok, count in ranking]
        if not len(ranking):
            ranking = ["SINGLETON:{}".format(file_hash)]
        ranking = ",".join(ranking)
        return "\t".join([file_hash, str(len(report["scans"])), ranking])
