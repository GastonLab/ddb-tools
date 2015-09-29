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
    return annotations


def read_genotypes(infile, genotypes, snp_annotations):
    num_snps = 0
    num_homozyous = 0
    num_xym = 0
    missing_snps = defaultdict(int)
    with open(infile, 'rU') as input:
        reader = csv.reader(input, dialect='excel-tab')
        for row in reader:
            if snp_annotations[row[0]]:
                # print snp_annotations[row[0]]['chr']
                if 1 <= int(snp_annotations[row[0]]['chr']) <= 22:
                    genotype = row[1].split('|')
                    genotypes[file][row[0]] = genotype[0]
                    num_snps += 1
                    if genotype[0] == 'AA' or genotype[0] == 'BB':
                        num_homozyous += 1
                else:
                    num_xym += 1
            else:
                if missing_snps[row[0]]:
                    pass
                else:
                    missing_snps[row[0]] += 1
                # sys.stderr.write("ERROR: SNP %s was not found in annotations file\n" % row[0])
            num_snps += 1
    percent_homozygous = (float(num_homozyous) / float(num_snps)) * 100
    sys.stdout.write("%s: %s percent homozygous\n" % (infile, percent_homozygous))
    sys.stdout.write("There were %s SNPs missing from the annotations file and skipped (%s percent)\n" %
                     (len(missing_snps), (len(missing_snps) / float(num_snps))))
    sys.stdout.write("Skipped %s snps not on 22 autosomes\n" % num_xym)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infiles', help="comma separated list of file names")
    parser.add_argument('-a', '--annotations', help="Annotations file with chromosomal locations of SNPs")
    parser.add_argument('-o', '--outfile', help="Output file name")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    sys.stdout.write("Reading annotations file: %s\n" % args.annotations)
    snp_annotations = read_annotation_file(args.annotations)

    sys.stdout.write("Reading genotype files\n")
    files = args.infiles.split(",")
    genotypes = defaultdict(lambda: defaultdict(int))
    for infile in files:
        read_genotypes(infile, genotypes, snp_annotations)

    # Need to change this to doing all pairwise comparisons using itertools
    # for infile in files:
    #    pass
