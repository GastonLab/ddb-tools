#!/usr/bin/env python

import sys
import argparse

from collections import defaultdict

# This script converts an AB formatted output file from Illumina GenomeStudio and converts it to a format
# readable by the HH program. Input is tab delimited with column 1 being the sample name, column 2 is the SNP name,
# and columns 3 and 4 are the alleles in AB format.


def parse_illumina_multi_abformat(infile):
    sample_genotypes_dict = defaultdict(dict)
    samples = list()
    parsing = 0
    with open(infile, 'rU') as input:
        lines = input.readlines()
        for line in lines:
            if line.startswith("[Data]"):
                parsing += 1
                continue
            if parsing == 1:
                samples = line.split()
                samples.pop(0)
                print samples
                parsing += 1
            if parsing == 2:
                    line_data = line.split()
                    rsid = line_data.pop(0)
                    for idx, sample in enumerate(samples):
                        sample_genotypes_dict[sample][rsid] = line_data[idx]

    return sample_genotypes_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input AB format genotyping file [Required]")
    parser.add_argument('-o', '--outfile', help="Output root AB format genotyping file for HH program [Required]")

    args = parser.parse_args()

    sys.stdout.write("Converting file %s to format for HH analysis program and outputting to %s\n" %
                     (args.infile, args.outfile))
    data = parse_illumina_multi_abformat(args.infile)

    for sample in data:
        with open("{}.{}.txt".format(sample, args.outfile), 'w') as output:
            for snp in data[sample]:
                output.write("%s\t%s\n" % (snp, data[sample][snp]))

    sys.stdout.write("Finished\n")
