#!/usr/bin/env python

import sys
import argparse

from cyvcf2 import VCF
from ddb import vcf_parsing
from ddb import configuration
from collections import defaultdict


def process_sample(parse_functions, sample, samples, config, snp_list):
    caller_records = defaultdict(lambda: dict())

    sys.stdout.write("Parsing Caller VCF Files\n")
    vcf_parsing.parse_vcf("{}.mutect.normalized.vcf".format(sample),
                          "mutect", caller_records)
    vcf_parsing.parse_vcf("{}.vardict.normalized.vcf".format(sample),
                          "vardict", caller_records)
    vcf_parsing.parse_vcf("{}.freebayes.normalized.vcf".format(sample),
                          "freebayes", caller_records)
    vcf_parsing.parse_vcf("{}.scalpel.normalized.vcf".format(sample),
                          "scalpel", caller_records)
    vcf_parsing.parse_vcf("{}.platypus.normalized.vcf".format(sample),
                          "platypus", caller_records)
    vcf_parsing.parse_vcf("{}.pindel.normalized.vcf".format(sample),
                          "pindel", caller_records)

    annotated_vcf = "{}.vcfanno.snpEff.GRCh37.75.vcf".format(sample)

    sys.stdout.write("Parsing VCFAnno VCF\n")
    vcf = VCF(annotated_vcf)

    sys.stdout.write("Processing individual variants\n")
    written_snp_count = 0
    written_snps = list()
    with open("{}.snp_freqs.txt".format(samples[sample]['library_name']),
              "w") as report:
        report.write("Chrom\tStart\tStop\tSNP ID\tSomatic AF\tDepth\tCallers\n")
        for variant in vcf:
            if variant.ID in snp_list:
                written_snp_count += 1
                written_snps.append(variant.ID)
                # Parsing VCF and creating data structures for Cassandra model
                callers = variant.INFO.get('CALLERS').split(',')

                key = (unicode("chr{}".format(variant.CHROM)), int(variant.start),
                       int(variant.end), unicode(variant.REF), unicode(variant.ALT[0]))

                caller_variant_data_dicts = defaultdict(dict)
                max_som_aaf = -1.00
                max_depth = -1
                min_depth = 100000000

                for caller in callers:
                    caller_variant_data_dicts[caller] = parse_functions[caller](caller_records[caller][key])
                    if float(caller_variant_data_dicts[caller]['AAF']) > max_som_aaf:
                        max_som_aaf = float(caller_variant_data_dicts[caller]['AAF'])
                    if int(caller_variant_data_dicts[caller]['DP']) < min_depth:
                        min_depth = int(caller_variant_data_dicts[caller]['DP'])
                    if int(caller_variant_data_dicts[caller]['DP']) > max_depth:
                        max_depth = int(caller_variant_data_dicts[caller]['DP'])

                if min_depth == 100000000:
                    min_depth = -1

                report.write("{}\t{}\t{}\t{}\t{}\t{}\t{}"
                             "\n".format(variant.CHROM, variant.start,
                                         variant.end, variant.ID, max_som_aaf,
                                         max_depth, ",".join(callers)))
        not_found = 0
        for snp in snp_list:
            if snp not in written_snps:
                not_found += 1
                report.write(".\t.\t.\t{}\t.\t.\t.\n".format(snp))
    sys.stdout.write("Variant data for {} SNPS written for sample {}."
                     " {} SNPs not found.\n".format(written_snp_count,
                                                    sample, not_found))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--samples_file',
                        help="Input configuration file for samples")
    parser.add_argument('-c', '--configuration',
                        help="Configuration file for various settings")
    parser.add_argument('-l', '--list',
                        help="List file of SNPs to process")

    args = parser.parse_args()

    sys.stdout.write("Parsing configuration data\n")
    config = configuration.configure_runtime(args.configuration)

    sys.stdout.write("Parsing sample data\n")
    samples = configuration.configure_samples(args.samples_file, config)

    parse_functions = {'mutect': vcf_parsing.parse_mutect_vcf_record,
                       'freebayes': vcf_parsing.parse_freebayes_vcf_record,
                       'vardict': vcf_parsing.parse_vardict_vcf_record,
                       'scalpel': vcf_parsing.parse_scalpel_vcf_record,
                       'platypus': vcf_parsing.parse_platypus_vcf_record,
                       'pindel': vcf_parsing.parse_pindel_vcf_record}
    snps = list()

    with open(args.list, 'r') as fh:
        snps = [current_snp.rstrip() for current_snp in fh.readlines()]

    for sample in samples:
        sys.stdout.write("Processing sample {}\n".format(sample))
        process_sample(parse_functions, sample, samples, config, snps)
