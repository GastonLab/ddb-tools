#!/usr/bin/env python

import os
import sys
import fnmatch

from collections import defaultdict

if __name__ == "__main__":
    counts = defaultdict(int)
    for root, dirs, files in os.walk("."):
        for config_file in fnmatch.filter(files, "1*_M0373?.config"):
            sys.stderr.write("Reading file: {}\n".format(os.path.join(root, config_file)))
            with open(os.path.join(root, config_file).rstrip(), 'r') as data_file:
                for line in data_file.readlines():
                    if line.startswith("report: "):
                        temp = line.split(" ")
                        counts[temp[1].rstrip()] += 1
    sys.stderr.write("Type\tCount\n")
    for report_type in counts:
        sys.stdout.write("{}\t{}\n".format(report_type, counts[report_type]))
