#!/usr/bin/env python

import argparse
from pybedtools import BedTool

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--bed', help="BED file of target regions")
    parser.add_argument('-r', '--reference', help="Reference FASTA file")

    args = parser.parse_args()

    targets = BedTool(args.bed)

    for target in targets:
        
