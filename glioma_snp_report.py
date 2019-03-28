#!/usr/bin/env python

import re
import sys
import utils
import cyvcf2
import argparse

from cyvcf2 import VCF
from toil.job import Job
from ddb import vcf_parsing
from ddb import configuration
from ddb_ngsflow import pipeline
from collections import defaultdict


def process_sample(job, parse_functions, sample, samples, config, snp_list):
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

    sys.stdout.write("Parsing VCFAnno VCF with CyVCF2\n")
    reader = cyvcf2.VCFReader(annotated_vcf)
    desc = reader["ANN"]["Description"]
    annotation_keys = [x.strip("\"'") for x in re.split("\s*\|\s*", desc.split(":", 1)[1].strip('" '))]

    sys.stdout.write("Processing individual variants\n")
    written_snps = 0
    with open("{}.snp_freqs.txt".format(samples[sample]['library_name']),
              "r") as report:
        for variant in vcf:
            if variant.ID in snp_list:
                written_snps += 1
                # Parsing VCF and creating data structures for Cassandra model
                callers = variant.INFO.get('CALLERS').split(',')
                effects = utils.get_effects(variant, annotation_keys)
                top_impact = utils.get_top_impact(effects)
                population_freqs = utils.get_population_freqs(variant)
                amplicon_data = utils.get_amplicon_data(variant)

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

                report.write("{}\t{}\t{}\n".format(variant.ID, max_som_aaf,
                                                   max_depth,
                                                   ",".join(callers)))
    job.fileStore.logToMaster("Variant data for {} SNPS written for sample {}"
                              "\n".format(sample, written_snps))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--samples_file',
                        help="Input configuration file for samples")
    parser.add_argument('-c', '--configuration',
                        help="Configuration file for various settings")

    Job.Runner.addToilOptions(parser)
    args = parser.parse_args()
    args.logLevel = "INFO"

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

    root_job = Job.wrapJobFn(pipeline.spawn_batch_jobs, cores=1)

    for sample in samples:
        sample_job = Job.wrapJobFn(process_sample, parse_functions, sample,
                                   samples, config, cores=1)
        root_job.addChild(sample_job)

    # Start workflow execution
    Job.Runner.startToil(root_job, args)
