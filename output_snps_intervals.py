#!/usr/bin/env python

import sys
import csv
import argparse
import pybedtools
import argcomplete

from collections import defaultdict

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--samples_file', help="Tab delimited file of sample IDs and their genotype files")
    parser.add_argument('-i', '--intervals', help="BED format file of intervals to output genotypes for")
    parser.add_argument('-o', '--outroot', help="Root output file name. Each interval has its own file")
    parser.add_argument('-a', '--annotations', help="SNP annotations file")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    samples = defaultdict(dict)
    sample_ids = list()

    sys.stdout.write("Reading Annotations file\n")
    annotations = pybedtools.BedTool(args.annotations)

    sys.stdout.write("Reading intervals file")
    intervals = pybedtools.BedTool(args.intervals)

    sys.stdout.write("Getting file list for samples\n")
    with open(args.samples_file, 'r') as samples_file:
        reader = csv.reader(samples_file, dialect='excel-tab')
        for row in reader:
            samples[row[0]]['file'] = row[1]
            sample_ids.append(row[0])

    sys.stdout.write("Reading genotypes\n")
    for sample in sample_ids:
        sys.stdout.write("Reading genotypes for sample {}\n".format(sample))
        with open(samples[sample]['file'], 'r') as sample_genotypes:
            reader = csv.reader(sample_genotypes, dialect='excel-tab')
            for row in reader:
                samples[sample][row[0]] = row[1]

    sys.stdout.write("Processing intervals")
    for interval in intervals:
        sys.stdout.write("Processing interval {}:{}-{}"
                         "\n".format(interval.chrom, interval.start, interval.stop))
        snps_in_interval = annotations.intersect(interval, u=True)
        sys.stdout.write("Outputting genotypes for interval {}:{}-{}"
                         "\n".format(interval.chrom, interval.start, interval.stop))
        with open("{}-{}-{}.genotypes.txt".format(interval.chrom, interval.start, interval.stop), 'w') as genotypes_file:
            genotypes_file.write("SNP ID\tChromosome\tPosition")
            for sample in sample_ids:
                genotypes_file.write("\t{}".format(sample))
            genotypes_file.write("\n")

            for snp in snps_in_interval:
                genotypes_file.write("{}\t{}\t{}".format(snp.name, snp.chrom, snp.start))
                for sample in sample_ids:
                    genotypes_file.write("\t{}".format(samples[sample][snp.name]))
                genotypes_file.write("\n")
