#!/usr/bin/env python

import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file name")
    parser.add_argument('-o', '--output', help="Output file name", default="output.vcf")
    args = parser.parse_args()

    with open(args.output, 'w') as output:
        with open(args.input, 'r') as infile:
            reader = csv.reader(infile, dialect='excel-tab')
            for row in reader:
                output.write("{chr}\t{pos}\t{ref}\t{alt}\t.\t.\tVARINFO={info}\n".format(chr=row[4],
                                                                                         pos=row[5],
                                                                                         ref=row[7],
                                                                                         alt=row[8],
                                                                                         info=row[2]))
