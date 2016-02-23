__author__ = 'dgaston'

import sys
import csv
import argparse
import argcomplete
import pybedtools

from collections import defaultdict


def read_genotypes(infile, genotypes):
    with open(infile, 'rU') as input:
        reader = csv.reader(input, dialect='excel-tab')
        for row in reader:
            genotype = row[1].split('|')
            genotypes[row[0]][file] = genotype[0]


def group_concordant(snp_concordance):
    """Return BedTool of Intervals corresponding to Runs of Conserved HH between samples"""
    run = []
    result = [run]
    chrom = None
    for snp in snp_concordance:
        if snp[4] == 1 and (snp[0] == chrom or chrom is None):
            run.append(snp)
            if chrom is None:
                chrom = snp[0]
        else:
            if len(run) > 1:
                result.append(run)
            run = []
            chrom = snp[0]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infiles', help="comma separated list of AB format genotype file names")
    parser.add_argument('-o', '--outfile', help="Output BED file name")
    parser.add_argument('-a', '--annotations', help="SNP annotations file for genotyping array (BED format)")
    parser.add_argument('-t', '--threshold', help='The threshold, in cM, for RCHH size cutoff across samples')

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    files = args.infiles.split(",")

    sys.stdout.write("Reading annotations file: %s\n" % args.annotations)
    snps = pybedtools.BedTool(args.annotations)

    genotypes = defaultdict(lambda: defaultdict(int))

    for infile in files:
        sys.stdout.write("Reading input genotype file %s\n" % infile)
        read_genotypes(infile, genotypes)

    sys.stdout.write("Checking homozygous SNPs for identical genotypes across samples\n")
    snp_concordance = list()
    for snp in snps:
        if snp.chrom == "chrM" or snp.chrom == "chrX" or snp.chrom == "chrY":
            continue
        snp_genotypes = list()
        for infile in files:
            if genotypes[snp.name][infile] == 'AA' or genotypes[snp.name][infile] == 'BB':
                snp_genotypes.append(genotypes[snp.name][infile])
        if all(element == snp_genotypes[0] for element in snp_genotypes):
            try:
                interval = (snp.chrom, int(snp.start), int(snp.stop), snp.name, 1, float(snp[-1]))
            except ValueError:
                print snp
                sys.exit()
        else:
            try:
                interval = (snp.chrom, int(snp.start), int(snp.stop), snp.name, 0, float(snp[-1]))
            except ValueError:
                print snp
                sys.exit()
        snp_concordance.append(interval)

    sys.stdout.write("Identifying RCHHs\n")
    clustered = group_concordant(snp_concordance)
    sys.stdout.write("Checking thresholds of RCHHs and outputting\n")
    with open(args.outfile, 'w') as outfile:
        for cluster in clustered:
            bp_length = cluster[-1][2] - cluster[0][1]
            distance = cluster[-1][-1] - cluster[0][-1]
            if distance >= float(args.threshold):
                outfile.write("%s\t%s\t%s\t%s\n" % (cluster[0][0], cluster[0][1], cluster[-1][2], distance))
