__author__ = 'dgaston'

__author__ = 'dgaston'

import csv
import argparse
import argcomplete


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input regions in BED format")
    parser.add_argument('-o', '--outfile', help="Output file root name")

    argcomplete.autocomplete(parser)
    args = parser.parse_args()

    with open(args.infile, 'rU') as csvfile:
        with open(args.outfile, 'w') as outfile:
            reader = csv.reader(csvfile, dialect='excel-tab')
            writer = csv.writer(outfile, delimiter='\t')
            for row in reader:
                writer.writerow([row[1], row[2], row[3], row[0], row[4], row[5], row[7], row[8], row[9], row[10]])