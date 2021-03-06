#!/usr/bin/env python

__author__ = 'dgaston'

# This script takes the output of the HH analysis program and converts it to a BED-style format. Output also includes
# the size of the region in both cM and in Mega Bases

import sys
import argparse
import collections
from itertools import islice
from itertools import izip
from itertools import tee


def pairs(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a = iter(iterable)
    return izip(a, a)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input AB format genotyping file [Required]")
    parser.add_argument('-o', '--outfile', help="Output AB format genotyping file for HH program [Required]")

    args = parser.parse_args()

    sys.stdout.write("Converting HH file to BED file format\n")

    bed_regions = list()
    with open(args.outfile, 'w') as outfile:
        with open(args.infile, 'rU') as infile:
            lines = infile.readlines()
            for line1, line2 in pairs(lines):
                line1_data = line1.split("\t")
                line2_data = line2.split("\t")

                cm_size = float(line2_data[2]) - float(line1_data[2])
                mbp_size = (int(line2_data[1]) - int(line1_data[1])) / 1000000.00
                outfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (line1_data[0], line1_data[1], line2_data[1],
                                                                    mbp_size, cm_size, line1_data[4], line1_data[5],
                                                                    line1_data[6]))

    sys.stdout.write("Finished\n")
