#!/usr/bin/env python

import sys
import csv

from collections import defaultdict

if __name__ == "__main__":
    control_files = ["C1.isoforms.txt", "C2.isoforms.txt", "C3.isoforms.txt"]
    sample_files = ["S1.isoforms.txt", "S2.isoforms.txt", "S3.isoforms.txt"]

    variants = defaultdict(lambda: defaultdict(int))

    for control in control_files:
        sys.stdout.write("Reading variants from {}\n".format(control))
        with open(control, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            next(reader)
            for row in reader:
                variant = row[0]
                variants[variant]['row'] = row
                variants[variant]['controls'] += 1

    for sample in sample_files:
        sys.stdout.write("Reading variants from {}\n".format(sample))
        with open(sample, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            next(reader)
            for row in reader:
                variant = row[0]
                variants[variant]['row'] = row
                variants[variant]['samples'] += 1

    with open("isoform_counts.txt", 'w') as outfile:
        sys.stdout.write("Writing Results to file\n")
        outfile.write("Genes\tControl Count\tSample Count\n")
        for variant in variants:
            outfile.write("{}\t{}\t{}\n".format(variant, variants[variant]['controls'], variants[variant]['samples']))
