#!/usr/bin/env python

import csv
import argparse

from collections import Counter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input tab-delimited file from GEMINI tro scan")
    parser.add_argument('-o', '--output', help="Output file name to write multi-hit genes to")
    args = parser.parse_args()

    gene_counts = Counter()
    with open(args.input, 'r') as infile:
        reader = csv.DictReader(infile, dialect='excel-tab')
        for row in reader:
            gene_counts[row['gene']] += 1

    with open(args.output, 'w') as outfile:
        for gene in gene_counts:
            if gene_counts[gene] > 1:
                outfile.write("{}\n".format(gene))
