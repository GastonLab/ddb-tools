#!/usr/bin/env python

import argparse
import pyhgvs as hgvs
import hgvs.utils as hgvs_utils

from pygr.seqdb import SequenceFileDB


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input file")
    parser.add_argument('-r', '--ref', help="Genome reference FASTA")
    parser.add_argument('-o', '--outfile', help="Output file name")

    args = parser.parse_args()

    genome = SequenceFileDB(args.ref)
