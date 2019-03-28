#!/usr/bin/env python

import csv
import sys
import argparse
import subprocess as sub

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help="Input file, list of sample names and VCFs to operate on, tab-delimited")
    parser.add_argument('-t', '--tag', help="Optional tag to add to output files for", default="")
    args = parser.parse_args()

    with open(args.input, 'r') as csvfile:
        reader = csv.reader(csvfile, dialect='excel-tab')
        for row in reader:
            indel_command = "vcftools --recode --recode-INFO-all --keep-only-indels " \
                            "--vcf {vcf} --out {id}.{tag}.INDELs".format(vcf=row[1], id=row[0], tag=args.tag)
            snv_command = "vcftools --recode --recode-INFO-all --remove-indels " \
                          "--vcf {vcf} --out {id}.{tag}.SNVs".format(vcf=row[1], id=row[0], tag=args.tag)

            sys.stdout.write("Splitting SNVs and Indels for sample {}\n".format(row[0]))

            p = sub.Popen(indel_command, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
            output = p.communicate()
            code = p.returncode
            if code:
                raise RuntimeError("An error occurred when executing the commandline: {}. "
                                   "Please check the logfile {} for details\n".format(indel_command))

            p = sub.Popen(snv_command, stdout=sub.PIPE, stderr=sub.PIPE, shell=True)
            output = p.communicate()
            code = p.returncode
            if code:
                raise RuntimeError("An error occurred when executing the commandline: {}. "
                                   "Please check the logfile {} for details\n".format(snv_command))
