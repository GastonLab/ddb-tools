import csv
import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--infile', help="Input file")
    parser.add_argument('-o', '--outfile', help="Output file")
    args = parser.parse_args()

    with open(args.infile, 'r') as infile:
        with open(args.outfile, 'w') as outfile:
            reader = csv.reader(infile, dialect='excel-tab')
            for row in reader:
                temp = row[0].split('.')
                outfile.write("{}\n".format(temp[0]))
