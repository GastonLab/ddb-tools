#!/usr/bin/env python

import sys
import argparse
from Bio import SeqIO


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input FASTA filename")
    parser.add_argument('-o', '--output', help="Fixed output FASTA filename")
    args = parser.parse_args()

    sys.stdout.write("Reading input file {}\n".format(args.input))
    with open(args.input, 'r') as alignfh:
        alignment = SeqIO.parse(alignfh, 'fasta')

        sys.stdout.write("Writing FASTA to file {}\n".format(args.output))
        with open(args.output, 'w') as outfh:
            SeqIO.write(alignment, outfh, 'fasta')

    sys.stdout.write("Finished!\n")
