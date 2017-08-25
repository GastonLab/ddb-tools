#!/usr/bin/env python

import sys
import argparse
import argcomplete

from collections import defaultdict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input list of paths to configuration files")
    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    counts = defaultdict(int)

    with open(args.input, 'r') as infile:
        for config_file in infile.readlines():
            sys.stderr.write("Reading file: {}\n".format(config_file))
            with open(config_file, 'r') as data_file:
                for line in data_file.readlines():
                    if line.startswith("report: "):
                        temp = line.split(" ")
                        counts[temp[1]] += 1

    sys.stderr.write("Type\tCount\n")
    for report_type in counts:
        sys.stdout.write("{}\t{}\n".format(report_type, counts[report_type]))
