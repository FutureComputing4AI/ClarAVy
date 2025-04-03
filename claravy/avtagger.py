import os
import sys
import json
import math
import pickle
import random
import logging
import argparse
import fileinput
import functools
import itertools
import multiprocessing
import numpy as np
from UltraDict import UltraDict
from concurrent.futures import ProcessPoolExecutor

from claravy import DATA_DIR
from claravy.avparse import AVParse
from claravy.avstats import AVStats_Map, AVStats
from claravy.avalias import AVAlias
from claravy.taxonomy import *
from claravy.ibcc.IBCC import IBCC
from claravy.ibcc.utils import unique


random.seed(42)
logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger("ClarAVy")


def _dir_path(string):
    """Check if the input is a valid directory."""
    if string is None:
        return None
    elif os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)


def _file_path(string):
    """Check if the input is a valid file path."""

    if string is None:
        return None
    elif os.path.isfile(string):
        return string
    else:
        raise FileNotFoundError(string)


def line_batcher(scan_files, scan_dirs, batch_size):
    """Read JSON lines from all input files and directories, and return
    batches of JSON lines."""

    # Get list of all .jsonl files
    file_paths = set()
    if scan_files is not None:
        file_paths.update(set(scan_files))
    if scan_dirs is None:
        scan_dirs = []
    for scan_dir in scan_dirs:
        file_paths.update({os.path.join(scan_dir, file_name)
                           for file_name in os.listdir(scan_dir)})
    file_paths = sorted(file_paths)

    # Read JSON lines from .jsonl files and return them in batches
    with fileinput.input(file_paths) as f:
        batcher = itertools.zip_longest(*[f] * batch_size)
        for batch in batcher:
            if batch:
                yield batch
            else:
                raise StopIteration


def get_batch_stats(batch, av_parser, token_vocab):
    """Compute stats about a batch of AV scan reports."""

    av_stats_mapper = AVStats_Map(av_parser.supported_avs)
    for report_json in batch:
        report = av_parser.load_report(report_json)
        if not report:
            continue
        stats = av_parser.report_stats(report, token_vocab)
        av_stats_mapper.update_stats(stats)
    return av_stats_mapper


def process_batch(batch, av_parser):
    """Get tag rankings for a batch of AV scan reports."""

    shm_token_vocab = UltraDict(name="shm_token_vocab", create=False,
                                shared_lock=True)
    shm_alias_mapping = UltraDict(name="shm_alias_mapping", create=False,
                                  shared_lock=True)
    return av_parser.process_batch(batch, shm_token_vocab, shm_alias_mapping)


def main_cli():

    # Parse command-line options
    parser = argparse.ArgumentParser()

    # Input arguments
    parser.add_argument("-f", "--scan-file", type=_file_path, action="append",
                        help="Path to JSON Lines (.jsonl) file with AV scan " +
                        "report data to process.")
    parser.add_argument("-d", "--scan-dir", type=_dir_path, action="append",
                        help="Path to directory of .jsonl files with AV " +
                        "scan report data to process.")

    # Data file arguments
    parser.add_argument("-av", "--av-file", type=_file_path,
                        default=os.path.join(DATA_DIR, "default_avs.json"),
                        help="Path to supported AVs and AV correlations file.")
    parser.add_argument("-tax", "--tax-file", type=_file_path,
                        default=os.path.join(DATA_DIR, "default_taxonomy.txt"),
                        help="Path to the token taxonomy file.")
    parser.add_argument("-al", "--alias-file", type=_file_path,
                        default=os.path.join(DATA_DIR, "default_aliases.txt"),
                        help="Path to the token alias mapping.")
    parser.add_argument("-su", "--substr-file", type=_file_path,
                        default=os.path.join(DATA_DIR, "default_substr.txt"),
                        help="Path to the token substring file.")
    parser.add_argument("-bl", "--ignore-file", type=_file_path,
                        default=os.path.join(DATA_DIR, "default_ignore.txt"),
                        help="Path to the token substring file.")
    parser.add_argument("-cm", "--confidence-model", type=_file_path,
                        default=os.path.join(DATA_DIR, "confidence_model.pkl"),
                        help="Path to the family label confidence model.")

    # Output arguments
    parser.add_argument("-o", "--out-file", type=str, default=None,
                        help="File to write output to.")
    parser.add_argument("-ox", "--out-tax-file", type=str, default=None,
                        help="File to write the generated token taxonomy to " +
                        "(if provided).")
    parser.add_argument("-oa", "--out-alias-file", type=str, default=None,
                        help="File to write the generated alias mapping to " +
                        "(if provided).")

    # Voting threshold arguments
    parser.add_argument("-bt", "--beh-threshold", type=int, default=5,
                        help="Number of votes needed to output a BEH token")
    parser.add_argument("-ft", "--file-threshold", type=int, default=5,
                        help="Number of votes needed to output a FILE token")
    parser.add_argument("-vt", "--vuln-threshold", type=int, default=1,
                        help="Number of votes needed to output a VULN token")
    parser.add_argument("-pt", "--pack-threshold", type=int, default=1,
                        help="Number of votes needed to output a PACK token")
    parser.add_argument("-gt", "--grp-threshold", type=int, default=1,
                        help="Number of votes needed to output a GRP token")

    # Miscellaneous arguments
    parser.add_argument("-hash", "--hash-format", default="md5",
                        choices=["md5", "sha1", "sha256"],
                        help="Hash format to use in output")
    parser.add_argument("--plurality-vote", default=False, action="store_true",
                        help="Use plurality voting instead of SparseIBCC")
    parser.add_argument("--num-processes", type=int, default=1,
                        help="The number of processes for multiprocessing")
    parser.add_argument("--batch-size", type=int, default=1000,
                        help="The number of scan reports to process per batch")
    args = parser.parse_args()

    # Validate arguments
    if args.scan_file is None and args.scan_dir is None:
        logger.warning("Use -f to input a .jsonl file or -d to input a " +
                       "directory of .jsonl files")
        exit(1)

    # Create AV parser
    vote_thresholds = {
        GRP: args.grp_threshold,
        CAT: args.beh_threshold,
        FILE: args.file_threshold,
        VULN: args.vuln_threshold,
        PACK: args.pack_threshold
    }

    # Object for parsing AV scan data
    av_parser = AVParse(args.av_file, args.ignore_file, vote_thresholds,
                        args.hash_format)
    token_vocab = av_parser.read_vocab(args.tax_file)

    # Parse AV scan reports in batches
    batcher = line_batcher(args.scan_file, args.scan_dir, args.batch_size)
    map_func = functools.partial(get_batch_stats, av_parser=av_parser,
                                 token_vocab=token_vocab)

    # Compute stats about AV labels in scan reports
    # Uses ProcessPoolExecutor to process batches of AV scans in parallel
    av_stats = AVStats(av_parser.supported_avs)
    mp_context = multiprocessing.get_context("spawn")
    input_left = True
    total_batches = 0
    N = 0 # Number of scan reports
    while input_left:
        batches = itertools.islice(batcher, args.num_processes)
        with ProcessPoolExecutor(max_workers=args.num_processes,
                                 mp_context=mp_context) as batch_exec:
            results = batch_exec.map(map_func, batches)
        num_batches = 0
        for av_stats_mapper in results:
            av_stats.reduce_stats(av_stats_mapper)
            num_batches += 1
            N += av_stats_mapper.num_scans
        if num_batches < args.num_processes:
            input_left = False
        total_batches += num_batches
        if num_batches > 0:
            msg = "Computed stats for {} total batches of scan reports"
            logger.info(msg.format(total_batches))

    # Finalize token vocab and token stats
    token_vocab, alias_mapping = av_parser.read_aliases(args.alias_file,
                                                        token_vocab)
    token_vocab, token_av_counts = av_parser.update_vocab(av_stats,
                                                          token_vocab)
    av_stats.update_token_stats(token_vocab, alias_mapping,
                                av_parser.correlated_avs,
                                av_parser.new_fam_tokens)
    av_parser.update_av_heur_labels(av_stats.av_heur_labels)
    logger.info("Finished computing statistics about scan reports")

    # Resolve aliases using the stats computed about tokens in AV labels
    av_alias = AVAlias(av_stats, token_vocab, av_parser, alias_mapping,
                       args.substr_file)
    alias_mapping = av_alias.alias_mapping
    token_vocab = av_alias.token_vocab

    # Write generated token vocab to file
    if args.out_tax_file is not None:
        av_parser.write_vocab(args.out_tax_file, token_vocab)
        logger.info("Wrote token taxonomy to {}".format(args.out_tax_file))

    # Write alias mapping to file
    if args.out_alias_file is not None:
        av_alias.write_alias_mapping(args.out_alias_file)
        logger.info("Wrote alias mapping to {}".format(args.out_alias_file))

    # Use UltraDict to support sharing token_vocab between processes.
    # Treated as read-only from this point on.
    token_dump_size = sys.getsizeof(token_vocab) + 1000
    UltraDict.unlink_by_name("shm_token_vocab", ignore_errors=True)
    UltraDict.unlink_by_name("shm_token_vocab_memory", ignore_errors=True)
    shm_token_vocab = UltraDict(token_vocab, name="shm_token_vocab",
                                buffer_size=token_dump_size,
                                create=True, shared_lock=True)

    # Use UltraDict to support sharing alias_mapping memory between processes.
    # Treated as read-only from this point on.
    alias_dump_size = sys.getsizeof(alias_mapping) + 1000
    UltraDict.unlink_by_name("shm_alias_mapping", ignore_errors=True)
    UltraDict.unlink_by_name("shm_alias_mapping_memory", ignore_errors=True)
    shm_alias_mapping = UltraDict(alias_mapping, name="shm_alias_mapping",
                                  buffer_size=alias_dump_size,
                                  create=True, shared_lock=True)

    # Function for getting tag ranking and family votes for each AV scan
    batcher = line_batcher(args.scan_file, args.scan_dir, args.batch_size)
    map_func = functools.partial(process_batch, av_parser=av_parser)

    # Map each AV product to a unique ID and vice-versa
    # Map each family to a unique ID and vice-versa
    idx_avs = sorted(av_stats.supported_avs)
    av_idxs = {av: idx for idx, av in enumerate(idx_avs)}
    idx_fams = []
    fam_idxs = {}
    L = 0
    K = len(av_idxs)

    # Output tagging results and track family annotations
    C = np.zeros((N, K), dtype=np.int32) - 1
    X = np.zeros((N, 7), dtype=np.float64)
    W = np.array(av_parser.av_weights, dtype=np.float64)
    confidence_scores = np.zeros(N, dtype=np.float64)
    detect_ratios = []
    hashes = []
    ratios = []
    tags = []
    input_left = True
    total_batches = 0

    i = 0
    while input_left:
        batches = itertools.islice(batcher, args.num_processes)
        with ProcessPoolExecutor(max_workers=args.num_processes,
                                 mp_context=mp_context) as batch_exec:
            results = batch_exec.map(map_func, batches)

        num_batches = 0
        for b_hashes, b_tags, b_families, b_features, b_detects in results:
            hashes += b_hashes
            tags += b_tags
            ratios += b_detects
            for file_hash, fams, features in zip(b_hashes, b_families,
                                                 b_features):

                # Assign IDs to new families
                fam_list = fams.keys()
                for family in fam_list:
                    if fam_idxs.get(family) is None:
                        idx_fams.append(family)
                        fam_idxs[family] = L
                        L += 1

                # Sample from correlated AVs that vote for the same family
                for family, avs in fams.items():
                    fam_idx = fam_idxs[family]
                    skip_avs = set()
                    avs = list(avs)
                    random.shuffle(avs)
                    for cur_av in avs:
                        if cur_av in skip_avs:
                            continue
                        corr_avs = av_parser.correlated_avs[cur_av]
                        corr_avs.add(cur_av)
                        skip_avs.update(corr_avs)
                        av_idx = av_idxs[cur_av]
                        C[i,av_idx] = fam_idx

                X[i, :] = features
                i += 1

            # Finished the current batch
            num_batches += 1

        # Check if we have processed all batches
        if num_batches < args.num_processes:
            input_left = False
        total_batches += num_batches
        if num_batches > 0:
            msg = "Re-parsed {} total batches of scan reports"
            logger.info(msg.format(total_batches))
    logger.info("Finished re-parsing scan reports")

    # Track idxs of families that were auto-identified
    new_fam_idxs = set()
    for fam in av_parser.new_fam_tokens:
        if fam_idxs.get(fam) is None:
            continue
        fam_idx = fam_idxs[fam]
        new_fam_idxs.add(fam_idx)

    # Identify families that are almost never the plurality
    plur_fams = []
    plur_counts = []
    fam_plur = {fam_idx: 0 for fam_idx in new_fam_idxs}
    fam_total = {fam_idx: 0 for fam_idx in new_fam_idxs}
    for i in range(N):
        scan = C[i]
        labels, counts = np.unique(scan[scan != -1], return_counts=True)
        if not len(counts):
            plur_fams.append(-1)
            plur_counts.append(0)
            continue

        # If there are ties, choose plurality randomly
        shuffled_idxs = list(range(len(labels)))
        random.shuffle(shuffled_idxs)
        labels = labels[shuffled_idxs]
        counts = counts[shuffled_idxs]

        max_count = max(counts)
        plur_fam = -1
        for label, count in zip(labels, counts):
            if fam_plur.get(label) is None:
                fam_plur[label] = 0
                fam_total[label] = 0
            if count == max_count:
                plur_fam = label
                fam_plur[label] += 1
            fam_total[label] += 1
        plur_fams.append(plur_fam)
        plur_counts.append(max_count)

    # Remove annotations with those families
    for fam_idx in new_fam_idxs:
        total = fam_total[fam_idx]
        plur = fam_plur[fam_idx]

        # Criteria for removal: plurality less than 10% of the time
        if total >= 1 and plur / total <= 0.1:
            C[C==fam_idx] = -1

    # Plurality voting - write output
    if args.plurality_vote:
        f = sys.stdout
        if args.out_file is not None:
            f = open(args.out_file, "w")
        for scan_idx, file_hash in enumerate(hashes):
            tag_str = tags[scan_idx]
            detect_ratio = ratios[scan_idx]
            most_likely_fam = plur_fams[scan_idx]
            plur_count = plur_counts[scan_idx]
            if most_likely_fam == -1:
                family = "SINGLETON:{}".format(file_hash)
            else:
                family = idx_fams[most_likely_fam]
            fam_str = "FAM:{}|{}".format(family, plur_count)
            msg = "{}\t{}\t{}".format(file_hash, detect_ratio, fam_str)
            if len(tag_str):
                msg += ",{}".format(tag_str)
            f.write(msg + "\n")

    # SparseIBCC
    else:
        ibcc_model = IBCC(
            L=L+1,
            K=K,
            W=W,
            max_iter=1,
            eps=0.01,
            beta0_factor = N / 100,
            n_jobs = args.num_processes,
            verbose=True,
        )
        posterior, preds, pred_probs = ibcc_model.fit_predict(C)

        # Update features with posterior
        for scan_idx in range(len(hashes)):
            most_likely_prob = 0.0
            pred_entropy = 0.0
            for _, prob in posterior[scan_idx]:
                if prob > most_likely_prob:
                    most_likely_prob = prob
                if prob == 0:
                    continue
                log_prob = math.log(prob)
                pred_entropy -= prob * log_prob
            X[scan_idx, 5] = most_likely_prob
            X[scan_idx, 6] = pred_entropy

        # Get confidence scores
        with open(args.confidence_model, "rb") as f:
            confidence_model = pickle.load(f)
        confidence_scores = confidence_model.predict_proba(X)

        # Write SparseIBCC output
        f = sys.stdout
        if args.out_file is not None:
            f = open(args.out_file, "w")
        for scan_idx, file_hash in enumerate(hashes):
            scan_posterior = posterior[scan_idx]
            tag_str = tags[scan_idx]
            detect_ratio = ratios[scan_idx]
            most_likely_fam = -1
            most_likely_prob = 0.0
            for fam, prob in scan_posterior:
                if prob > most_likely_prob:
                    most_likely_fam = fam
                    most_likely_prob = prob
            if most_likely_fam == -1:
                family = "SINGLETON:{}".format(file_hash)
                confidence = 0.0
            else:
                family = idx_fams[most_likely_fam]
                confidence = float(confidence_scores[scan_idx, 1]) * 100
            fam_str = "FAM:{}|{:.2f}%".format(family, confidence)
            msg = "{}\t{}\t{}".format(file_hash, detect_ratio, fam_str)
            if len(tag_str):
                msg += ",{}".format(tag_str)
            f.write(msg + "\n")

    if args.out_file is None:
        args.out_file = "stdout"
    else:
        f.close()
    logger.info("Wrote {} results to {}".format(len(hashes), args.out_file))

if __name__ == "__main__":
    main_cli()
