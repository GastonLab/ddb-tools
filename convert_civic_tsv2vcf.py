#!/usr/bin/env python

import argparse
import csv

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file name")
    parser.add_argument('-o', '--output', help="Output file name", default="output.vcf")
    args = parser.parse_args()

    with open(args.output, 'w') as output:
        output.write("##fileformat=VCFv4.2\n")
        output.write("""##INFO=<ID=CIVIC_VARTYPE,Number=1,Type=String,Description="CiVic Variation Type">\n""")
        output.write("""##INFO=<ID=CIVIC_INFO,Number=1,Type=String,Description="CiVic Variation Info">\n""")
        output.write("""##INFO=<ID=CIVIC_VARGROUP,Number=1,Type=String,Description="CiVic Variation Group">\n""")
        with open(args.input, 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            reader.next()
            for row in reader:
                if len(row) >= 10:
                    if any([row[8], row[9]]):
                        output.write("{chr}\t{pos}\t{ref}\t{alt}\t.\t.\t"
                                     "CIVIC_VARTYPE='{type}';CIVIC_INFO='{info}'\t"
                                     "CIVIC_VARGROUP='{group}'\n".format(chr=row[5], pos=row[6], ref=row[8], alt=row[9],
                                                                         type=row[2], info=row[3], group=row[4]))
