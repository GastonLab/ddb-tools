#!/usr/bin/env python

import argparse
import csv
import sys

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
        with open(args.input, 'rU') as infile:
            reader = csv.reader(infile, delimiter='\t')
            reader.next()
            for row in reader:
                # sys.stdout.write("Processing row: {}".format(",".join(row)))
                if row[2] not in ("OVEREXPRESSION", "ITD", "BCR-ABL", "EML4-ALK"):
                    output.write("{chr}\t{pos}\t{ref}\t{alt}\t.\t.\t"
                                 "CIVIC_GENE='{gene}';CIVIC_VAR='{var}';CIVIC_DIS='{dis}';CIVIC_DOID='{doid}';"
                                 "CIVIC_DRUGS='{drug}';CIVIC_TYPE='{type}';CIVIC_DIRECTION='{dir}';"
                                 "CIVIC_LEVEL='{level}';CIVIC_SIG='{sig}';CIVIC_STATEMENT='{state}';"
                                 "CIVIC_PUBMED='{pubmed}';CIVIC_CITE='{cite}';CIVIC_RATE='{rate}';"
                                 "CIVIC_STATUS='{status}';CIVIC_SUMMARY='{sum}'\t"
                                 "\n".format(chr=row[18], pos=row[19], ref=row[21], alt=row[22], gene=row[0],
                                             var=row[2], dis=row[3], doid=row[4], drug=row[5], type=row[6],
                                             dir=row[7], level=row[8], sig=row[9], state=row[10], pubmed=row[11],
                                             cite=row[12], rate=row[13], status=row[14], sum=row[28]))
