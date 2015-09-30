__author__ = 'dgaston'

import argparse
import argcomplete

import pybedtools


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="input file (BED)")
    parser.add_argument('-o', '--outfile', help="Output file (GATK interval list)")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    