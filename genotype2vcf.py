__author__ = 'dgaston'

import argparse
import argcomplete
import csv
import sys
import datetime
from collections import defaultdict


def create_vcf_header(sample_id):
    date = datetime.date.today()
    header = "##fileformat=VCFv4.1\n" \
             "##fileDate=%s-%s-%s\n" \
             "##source=genotype2vcf.py\n" \
             "#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t%s\n" % (date.year, date.month, date.day, sample_id)

    return header


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
        header = create_vcf_header(infile)
        output.write(header)
        with open(infile, 'rU') as input:
            reader = csv.reader(input, dialect='excel-tab')
            for row in reader:
                if snp_annotations[row[0]]:
                    if 1 <= int(snp_annotations[row[0]]['chr']) <= 22:
                        genotype_data = row[1].split('|')
                        if genotype_data[0] == "AA" or genotype_data[0] == "BB":
                            genotype = "1/1"
                        else:
                            genotype = "0/1"
                        output.write("%s\t%s\t%s\t.\t.\t.\t.\t.\tGT\t%s\n" % (snp_annotations[row[0]]['chr'],
                                                                              snp_annotations[row[0]]['pos'],
                                                                              row[0], genotype))


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
