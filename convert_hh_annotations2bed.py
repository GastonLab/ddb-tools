#!/usr/bin/env python

import csv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input annotations file for HH program")
    parser.add_argument('-o', '--outfile', help="Output BED format file name")

    args = parser.parse_args()

    with open(args.infile, 'rU') as csvfile:
        with open(args.outfile, 'w') as outfile:
            reader = csv.reader(csvfile, dialect='excel-tab')
            for row in reader:
                outfile.write("%s\t%s\t%s\t%s\n" % (row[0], row[1], row[1], row[3]))
