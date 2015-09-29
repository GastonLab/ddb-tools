__author__ = 'dgaston'

import argparse
import argcomplete
import csv
import sys
from collections import defaultdict


def read_annotation_file(infile):
    annotations = defaultdict(dict)
    with open(infile, 'rU') as input:
        reader = csv.reader(input, dialect='excel-tab')
        for row in reader:
            annotations[row[3]]['chr'] = row[0]
            annotations[row[3]]['pos'] = row[1]
            annotations[row[3]]['loc'] = row[4]
    return annotations


def convert_genotypes(infile, outfile, snp_annotations):
    with open(outfile, 'w') as output:
        with open(infile, 'rU') as input:
            reader = csv.reader(input, dialect='excel-tab')
            for row in reader:
                if snp_annotations[row[0]]:
                    # print snp_annotations[row[0]]['chr']
                    if 1 <= int(snp_annotations[row[0]]['chr']) <= 22:
                        genotype = row[1].split('|')
                        output.write("%s\t%s\t%s\t%s\t%s\n" % (snp_annotations[row[0]]['chr'],
                                                               int(snp_annotations[row[0]]['pos']) - 1,
                                                               snp_annotations[row[0]]['pos'],
                                                               snp_annotations[row[0]]['loc'],
                                                               genotype[0]))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="input file names")
    parser.add_argument('-a', '--annotations', help="Annotations file with chromosomal locations of SNPs")
    parser.add_argument('-o', '--outfile', help="Output file name")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    sys.stdout.write("Reading annotations file: %s\n" % args.annotations)
    snp_annotations = read_annotation_file(args.annotations)

    sys.stdout.write("Reading and converting genotype files\n")
    convert_genotypes(args.infile, args.outfile, snp_annotations)
