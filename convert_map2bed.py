__author__ = 'dgaston'

import csv
import argparse
import argcomplete


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input file (Genetic Map file from HapMap)")
    parser.add_argument('-o', '--outfile', help="Output BED file name")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    with open(args.outfile, 'w') as output:
        with open(args.infile, 'rb') as infile:
            reader = csv.reader(infile, dialect='excel-tab')
            reader.next()
            for row in reader:
                # print row
                output.write("%s\t%s\t%s\t%s\n" % (row[0], int(row[1]) - 1, row[1], row[3]))
