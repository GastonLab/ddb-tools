#!/usr/bin/env python

import sys
import argparse
import HTSeq
from collections import defaultdict
from ddb import configuration


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input config file for samples")
    parser.add_argument('-o', '--output', help="Output file name for CSV file")
    args = parser.parse_args()

    config = dict()
    sys.stdout.write("Parsing sample data\n")
    samples = configuration.configure_samples(args.samples_file, config)

    transcript_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

    for sample in samples:
        gtf_file = HTSeq.GFF_Reader(sample['gtf'], end_included=True)
