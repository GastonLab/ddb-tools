#!/usr/bin/env python

import os
import sys
import cyvcf2
import argparse

from ddb_ngsflow import pipeline
from ddb import vcf_parsing
from cyvcf2 import VCF
from cyvcf2 import Writer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sample',
                        help="Sample name")
    parser.add_argument('-c', '--caller',
                        help="Name of caller to use")
    args = parser.parse_args()
    args.logLevel = "INFO"

    input_vcf = "{}.{}.normalized.vcf".format(args.sample, args.caller)
    output_vcf = "{}.{}.low_qual_filtered.vcf".format(args.sample, args.caller)

    sys.stdout.write("Filtering VCF {}\n".format(input_vcf))
    parse_functions = {'mutect': vcf_parsing.parse_mutect_vcf_record,
                       'freebayes': vcf_parsing.parse_freebayes_vcf_record,
                       'vardict': vcf_parsing.parse_vardict_vcf_record,
                       'scalpel': vcf_parsing.parse_scalpel_vcf_record,
                       'platypus': vcf_parsing.parse_platypus_vcf_record,
                       'pindel': vcf_parsing.parse_pindel_vcf_record}

    vcf = VCF(input_vcf)
    writer = Writer(output_vcf, vcf)

    for variant in vcf:
        pass_filter = True
        var_info = parse_functions[args.caller](variant)
        if int(var_info['Alt_Depth']) < 5:
            pass_filter = False
        if pass_filter:
            writer.write_record(variant)

    writer.close()
    vcf.close()
