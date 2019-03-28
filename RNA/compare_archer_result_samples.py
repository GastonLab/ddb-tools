#!/usr/bin/env python

import sys
import csv

from collections import defaultdict

if __name__ == "__main__":
    control_files = ["C1.variants.txt", "C2.variants.txt", "C3.variants.txt"]
    sample_files = ["S1.variants.txt", "S2.variants.txt", "S3.variants.txt"]

    variants = defaultdict(lambda: defaultdict(int))

    for control in control_files:
        sys.stdout.write("Reading variants from {}\n".format(control))
        with open(control, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            next(reader)
            for row in reader:
                variant = row[2]
                variants[variant]['row'] = row
                variants[variant]['controls'] += 1

    for sample in sample_files:
        sys.stdout.write("Reading variants from {}\n".format(sample))
        with open(sample, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            next(reader)
            for row in reader:
                variant = row[2]
                variants[variant]['row'] = row
                variants[variant]['samples'] += 1

    sys.stdout.write("Writing results to file\n")
    with open("variant_counts.txt", 'w') as outfile:
        outfile.write("Variant\tControl Count\tSample Count\n")
        for variant in variants:
            outfile.write("{}\t{}\t{}\n".format(variant, variants[variant]['controls'], variants[variant]['samples']))
