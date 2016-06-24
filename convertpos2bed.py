#!/usr/bin/env python

import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file name")
    parser.add_argument('-o', '--output', help="Output file name", default="output.bed")
    args = parser.parse_args()

    with open(args.output, 'w') as output:
        with open(args.input, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            reader.next()
            for row in reader:
                sections = row[0].split(':')
                output.write("{}\t{}\t{}\n".format(sections[0], sections[1], int(sections[1]) + 1))
