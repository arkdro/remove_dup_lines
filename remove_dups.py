#!/usr/bin/env python3

# Reads lines from a file, removes approximate duplicates, writes result to a file.
# Uses a sliding window to keep track of last N lines.

import argparse
import jellyfish
import logging
import re
import sys


SIMILARITY_LIMIT = 0.94
SLIDING_WINDOW_SIZE = 5
NEWLINE = "\n"


def is_single_dup(limit, line, prev_line):
    similarity = jellyfish.jaro_winkler_similarity(line, prev_line)
    return similarity >= limit


def is_dup(limit, line, acc):
    return any([is_single_dup(limit, line, x) for x in acc])


def update_sliding_window(sliding_window_size, line, sliding_window):
    sliding_window.append(line)
    if len(sliding_window) > sliding_window_size:
        sliding_window.pop(0)


def update_accumulator(line, acc):
    acc.append(line)


def process_line(args, line, fd, acc, sliding_window):
    if is_dup(args.similarity, line, sliding_window):
        pass
    else:
        update_accumulator(line, acc)
        update_sliding_window(args.window, line, sliding_window)


def read_file_lines(fdi):
    lines = []
    for l in fdi.readlines():
        line_str = l.decode().rstrip()
        lines.append(line_str)
    return lines


def build_one_result_line(line):
    return (line + NEWLINE).encode()


def build_result(acc):
    return [build_one_result_line(x) for x in acc]


def iterate_over_lines(args, fdi, fdo):
    acc = []
    sliding_window = []
    lines = read_file_lines(fdi)
    sorted_lines = sorted(lines)
    for l in sorted_lines:
        process_line(args, l, fdo, acc, sliding_window)
    res_acc = build_result(acc)
    fdo.writelines(res_acc)


def process_input_file(args):
    if args.infile is not None:
        infile = args.infile
    else:
        infile = sys.stdin.fileno()
    if args.outfile is not None:
        outfile = args.outfile
    else:
        outfile = sys.stdout.fileno()
    with open(infile, 'rb') as fdi:
        with open(outfile, 'wb') as fdo:
            iterate_over_lines(args, fdi, fdo)


def main(args):
    process_input_file(args)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile')
    parser.add_argument('-o', '--outfile')
    parser.add_argument('-s', '--similarity', type=float, default=SIMILARITY_LIMIT)
    parser.add_argument('-w', '--window', type=int, default=SLIDING_WINDOW_SIZE)
    parser.add_argument('-d', '--debug', default='info')
    return parser.parse_args()


if __name__ == '__main__':
    arguments = get_args()
    debug_level = arguments.debug.upper()
    logging.basicConfig(format='%(asctime)s %(message)s', level=debug_level)
    main(arguments)
