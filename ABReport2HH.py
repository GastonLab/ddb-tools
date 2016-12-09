#!/usr/bin/env python

import sys
import argparse

# This script converts an AB formatted output file from Illumina GenomeStudio and converts it to a format
# readable by the HH program. Input is tab delimited with column 1 being the sample name, column 2 is the SNP name,
# and columns 3 and 4 are the alleles in AB format.


def parse_illumina_abformat(infile):
    genotype_dict = dict()
    parsing = 0
    with open(infile, 'rU') as input:
        lines = input.readlines()
        for line in lines:
            if line.startswith("[Data]"):
                parsing += 1
            elif line.startswith("Sample Name\tSNP Name\tAllele1 - AB\tAllele2 - AB"):
                parsing +=1
            else:
                if parsing == 2:
                    line_data = line.split()
                    genotype_dict[line_data[1]] = "%s%s" % (line_data[2], line_data[3])

    return genotype_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input AB format genotyping file [Required]")
    parser.add_argument('-o', '--outfile', help="Output AB format genotyping file for HH program [Required]")

    args = parser.parse_args()

    sys.stdout.write("Converting file %s to format for HH analysis program and outputting to %s\n" %
                     (args.infile, args.outfile))
    data = parse_illumina_abformat(args.infile)

    with open(args.outfile, 'w') as output:
        for snp_name in data:
            output.write("%s\t%s\n" % (snp_name, data[snp_name]))

    sys.stdout.write("Finished\n")
