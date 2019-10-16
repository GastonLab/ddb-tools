#!/usr/bin/env python

import sys
import argparse

from ddb import vcf_parsing
from cyvcf2 import VCF
from cyvcf2 import Writer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input',
                        help="Input file")
    parser.add_argument('-s', '--sample',
                        help="Sample name")
    parser.add_argument('-c', '--caller',
                        help="Name of caller to use")
    args = parser.parse_args()
    args.logLevel = "INFO"

    output_vcf = "{}.{}.low_qual_filtered.vcf".format(args.sample, args.caller)

    sys.stdout.write("Filtering VCF {}\n".format(args.input))
    parse_functions = {'mutect': vcf_parsing.parse_mutect_vcf_record,
                       'freebayes': vcf_parsing.parse_freebayes_vcf_record,
                       'vardict': vcf_parsing.parse_vardict_vcf_record,
                       'scalpel': vcf_parsing.parse_scalpel_vcf_record,
                       'platypus': vcf_parsing.parse_platypus_vcf_record,
                       'pindel': vcf_parsing.parse_pindel_vcf_record}

    sys.stdout.write("Opening input file\n")
    vcf = VCF(args.input)
    sys.stdout.write("Opening output file\n")
    writer = Writer(output_vcf, vcf)

    sys.stdout.write("Iterating through input VCF\n")
    for variant in vcf:
        pass_filter = True
        var_info = parse_functions[args.caller](variant)
        if float(var_info['Alt_Depth']) < 5.0:
            pass_filter = False
        if pass_filter:
            writer.write_record(variant)

    writer.close()
