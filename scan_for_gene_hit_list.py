#!/usr/bin/env python

import csv
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input tab-delimited file to scan")
    parser.add_argument('-l', '--list', help="File with list of genes to scan for")
    args = parser.parse_args()

    gene_list = list()
    with open(args.list, 'r') as listfile:
        reader = csv.reader(listfile, dialect='excel-tab')
        for row in reader:
            gene_list.append(row[0].replace('\n', '').replace('\r', ''))

    with open(args.input, 'r') as infile:
        reader = csv.DictReader(infile, dialect='excel-tab')
        for row in reader:
            if row['Gene'] in gene_list:
                print row['Gene']
