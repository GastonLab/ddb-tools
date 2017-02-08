#!/usr/bin/env python

import sys
import csv
import argparse
import pybedtools
import argcomplete

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--samples_file', help="Tab delimited file of sample IDs and their genotype files")
    parser.add_argument('-i', '--intervals', help="BED format file of intervals to output genotypes for")
    parser.add_argument('-o', '--outroot', help="Root output file name. Each interval has its own file")
    parser.add_argument('-a', '--annotations', help="SNP annotations file")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    samples = dict()

    sys.stdout.write("Reading Annotations file\n")
    annotations = pybedtools.BedTool(args.annotations)

    sys.stdout.write("Reading intervals file")
    intervals = pybedtools.BedTool(args.intervals)

    with open(args.samples_file, 'r') as samples_file:
        reader = csv.reader(samples_file, dialect='excel-tab')
        for row in reader:
            samples[row[0]] = row[1]
