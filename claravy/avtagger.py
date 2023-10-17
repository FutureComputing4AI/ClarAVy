import os
import sys
import logging
import argparse
import fileinput
import functools
import itertools
import multiprocessing
from UltraDict import UltraDict
from concurrent.futures import ProcessPoolExecutor
from claravy import DATA_DIR
from claravy.avparse import AVParse
from claravy.avstats import AVStats_Map, AVStats
from claravy.avalias import AVAlias
from claravy.taxonomy import *

logger = logging.getLogger("ClarAVy")
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.INFO)
stderr_handler.setFormatter(logging.Formatter(u"%(message)s"))
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(stderr_handler)


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
        file_paths.update(set([os.path.join(scan_dir, file_name)
                               for file_name in os.listdir(scan_dir)]))
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


def get_batch_ranking(batch, av_parser):
    """Get rankings for a batch of AV scan reports."""
    shm_token_vocab = UltraDict(name="shm_token_vocab", create=False,
                                shared_lock=True)
    shm_alias_mapping = UltraDict(name="shm_alias_mapping", create=False,
                                  shared_lock=True)
    batch_rankings = []
    for report_json in batch:
        report = av_parser.load_report(report_json)
        if not report:
            continue
        batch_rankings.append(av_parser.report_ranking(report, shm_token_vocab,
                                                       shm_alias_mapping))
    return batch_rankings


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
                        default=os.path.join(DATA_DIR, "default_avs.txt"),
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

    # Output arguments
    parser.add_argument("-o", "--out-file", type=str, default=None,
                        help="File to write results to (if provided). Else, " +
                        "results are written to stdout.")
    parser.add_argument("-ot", "--out-tax-file", type=str, default=None,
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

    # Miscellaneous arguments
    parser.add_argument("-hash", "--hash-format", default="md5",
                        choices=["md5", "sha1", "sha256"],
                        help="Hash format to use in output")
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
        CAT: args.beh_threshold,
        TGT: args.file_threshold,
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
    while input_left:
        batches = itertools.islice(batcher, args.num_processes)
        with ProcessPoolExecutor(max_workers=args.num_processes,
                                 mp_context=mp_context) as batch_exec:
            results = batch_exec.map(map_func, batches)
        num_batches = 0
        for av_stats_mapper in results:
            av_stats.reduce_stats(av_stats_mapper)
            num_batches += 1
        if num_batches < args.num_processes:
            input_left = False
        total_batches += num_batches
        if num_batches > 0:
            msg = "Computed stats for {} total batches of scan reports"
            logger.info(msg.format(total_batches))

    # Finalize token vocab and token stats
    token_vocab, alias_mapping = av_parser.read_aliases(args.alias_file,
                                                        token_vocab)
    token_vocab = av_parser.update_vocab(av_stats, token_vocab)
    av_stats.update_token_stats(token_vocab)
    logger.info("Finished computing statistics about scan reports")

    # Write generated token vocab to file
    if args.out_tax_file is not None:
        av_parser.write_vocab(args.out_tax_file, token_vocab)
        logger.info("Wrote token taxonomy to {}".format(args.out_tax_file))

    # Resolve aliases using the stats computed about tokens in AV labels
    av_alias = AVAlias(av_stats, token_vocab, alias_mapping, args.substr_file)
    alias_mapping = av_alias.alias_mapping

    # Write alias mapping to file
    if args.out_alias_file is not None:
        av_alias.write_alias_mapping(args.out_alias_file)
        logger.info("Wrote alias mapping to {}".format(args.out_alias_file))

    # Use UltraDict to support sharing token_vocab and alias_mapping memory
    # between processes. Treated as read-only from this point on.
    token_dump_size = sys.getsizeof(token_vocab) + 1000
    shm_token_vocab = UltraDict(token_vocab, name="shm_token_vocab",
                                buffer_size=token_dump_size,
                                create=True, shared_lock=True)
    alias_dump_size = sys.getsizeof(alias_mapping) + 1000
    shm_alias_mapping = UltraDict(alias_mapping, name="shm_alias_mapping",
                                  buffer_size=alias_dump_size,
                                  create=True, shared_lock=True)

    # Get ranking for each AV scan
    batcher = line_batcher(args.scan_file, args.scan_dir, args.batch_size)
    map_func = functools.partial(get_batch_ranking, av_parser=av_parser)

    # Delete result file if it exists
    if args.out_file is not None:
        with open(args.out_file, "w") as out_f:
            pass

    # Write results to file or stdout
    input_left = True
    total_batches = 0
    while input_left:
        batches = itertools.islice(batcher, args.num_processes)
        with ProcessPoolExecutor(max_workers=args.num_processes,
                                 mp_context=mp_context) as batch_exec:
            results = batch_exec.map(map_func, batches)
        out_f = sys.stdout
        if args.out_file is not None:
            out_f = open(args.out_file, "a+")
        num_batches = 0
        for result_batch in results:
            result_batch = "\n".join([result for result in result_batch if result is not None])
            if len(result_batch):
                out_f.write(result_batch + "\n")
            num_batches += 1
        if num_batches < args.num_processes:
            input_left = False
        if args.out_file is not None:
            out_f.close()
        total_batches += num_batches
        if num_batches > 0:
            msg = "Ranked {} total batches of scan reports"
            logger.info(msg.format(total_batches))


if __name__ == "__main__":
    main_cli()
