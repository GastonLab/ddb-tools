#!/usr/bin/env python

import os
import sys
import fnmatch

from ddb import configuration
from collections import defaultdict

if __name__ == "__main__":
    type = "colorectal"
    type_cases = defaultdict(defaultdict(list))
    counts = defaultdict(int)
    for root, dirs, files in os.walk("."):
        for config_file in fnmatch.filter(files, "1*_M0373?.config"):
            sys.stderr.write("Reading file: {}\n".format(os.path.join(root, config_file)))
            sys.stdout.write("Parsing sample data\n")
            libraries = configuration.configure_samples(args.samples_file,
                                                        os.path.join(root,
                                                                     config_file))
            samples = configuration.merge_library_configs_samples(libraries)
            for sample in samples:
                if sample['report'].startswith(type):
                    print "Colorectal case found: {}\n".format(sample)

    sys.stderr.write("Type\tCount\n")
    for report_type in counts:
        sys.stdout.write("{}\t{}\n".format(report_type, counts[report_type]))
